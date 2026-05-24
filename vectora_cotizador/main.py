"""Aplicación de escritorio: Vectora Cotizador.

Interfaz Tkinter minimalista para cotizar corte y grabado láser.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import load_config
from config import CONFIG
from calculator import QuoteInput, calculate_quote


class VectoraCotizadorApp:
    """Controlador principal de la interfaz."""

    WORK_TYPES = ["Corte", "Grabado", "Corte + Grabado"]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Vectora Cotizador")
        self.root.geometry("640x700")
        self.root.resizable(False, False)

        self.config = load_config()

        self._configure_style()
        self._build_ui()

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        default_font = ("Segoe UI", 11)
        heading_font = ("Segoe UI", 16, "bold")

        style.configure("TLabel", font=default_font)
        style.configure("TEntry", font=default_font)
        style.configure("TCombobox", font=default_font)
        style.configure("Title.TLabel", font=heading_font)
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=12)
        style.configure("Secondary.TButton", font=("Segoe UI", 11), padding=9)

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Vectora Cotizador", style="Title.TLabel").pack(anchor="w", pady=(0, 16))

        form = ttk.Frame(container)
        form.pack(fill="x")

        self.material_var = tk.StringVar()
        self.work_type_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.complexity_var = tk.StringVar()
        self.coverage_var = tk.StringVar()

        self._add_combo(form, "Material", self.material_var, list(self.config["materiales"].keys()), 0)
        self._add_combo(form, "Material", self.material_var, list(CONFIG["materiales"].keys()), 0)
        self._add_combo(form, "Tipo de trabajo", self.work_type_var, self.WORK_TYPES, 1)
        self._add_entry(form, "Cantidad", self.quantity_var, 2)
        self._add_entry(form, "Ancho (cm)", self.width_var, 3)
        self._add_entry(form, "Alto (cm)", self.height_var, 4)
        self._add_combo(form, "Complejidad de corte", self.complexity_var, list(self.config["factores_complejidad"].keys()), 5)
        self._add_combo(form, "Cobertura de grabado", self.coverage_var, list(self.config["factores_cobertura"].keys()), 6)
        self._add_combo(form, "Complejidad de corte", self.complexity_var, list(CONFIG["factores_complejidad"].keys()), 5)
        self._add_combo(form, "Cobertura de grabado", self.coverage_var, list(CONFIG["factores_cobertura"].keys()), 6)

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(18, 10))

        ttk.Button(actions, text="CALCULAR", style="Primary.TButton", command=self.calculate).pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="LIMPIAR", style="Secondary.TButton", command=self.clear_form).pack(fill="x")

        self.result_text = tk.Text(
            container,
            height=14,
            font=("Consolas", 11),
            padx=12,
            pady=12,
            state="disabled",
            bg="#fafafa",
        )
        self.result_text.pack(fill="both", expand=True, pady=(12, 0))

        # Valores iniciales para reducir fricción de uso.
        self.material_var.set("MDF 3 mm")
        self.work_type_var.set("Corte")
        self.complexity_var.set("Baja")
        self.coverage_var.set("Baja")

    def _add_combo(self, parent: ttk.Frame, label: str, variable: tk.StringVar, values: list[str], row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=6)
        combo = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", pady=6)
        parent.columnconfigure(1, weight=1)

    def _add_entry(self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=6)
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=6)

    def _read_numeric(self, value: str, field_name: str, integer: bool = False):
        if not value.strip():
            raise ValueError(f"El campo '{field_name}' es obligatorio.")

        try:
            number = int(value) if integer else float(value)
        except ValueError as exc:
            raise ValueError(f"El campo '{field_name}' debe ser numérico.") from exc

        if number < 0:
            raise ValueError(f"El campo '{field_name}' no puede ser negativo.")

        if integer and number == 0:
            raise ValueError(f"El campo '{field_name}' debe ser mayor a cero.")

        return number

    def calculate(self) -> None:
        try:
            quote_input = QuoteInput(
                material=self.material_var.get(),
                work_type=self.work_type_var.get(),
                quantity=self._read_numeric(self.quantity_var.get(), "Cantidad", integer=True),
                width_cm=self._read_numeric(self.width_var.get(), "Ancho"),
                height_cm=self._read_numeric(self.height_var.get(), "Alto"),
                cut_complexity=self.complexity_var.get(),
                engraving_coverage=self.coverage_var.get(),
            )

            if quote_input.width_cm == 0 or quote_input.height_cm == 0:
                raise ValueError("Ancho y alto deben ser mayores a cero.")

            result = calculate_quote(quote_input, self.config)
            result = calculate_quote(quote_input, CONFIG)
            self._show_result(result)

        except ValueError as error:
            messagebox.showerror("Validación", str(error))

    def _show_result(self, result) -> None:
        lines = [
            f"Área total: {result.area_total:.2f} cm²",
            "",
            f"Costo material: ${result.material_cost:,.2f}",
            f"Costo corte: ${result.cut_cost:,.2f}",
            f"Costo grabado: ${result.engraving_cost:,.2f}",
            f"Costo fijo: ${result.fixed_cost:,.2f}",
            "",
            f"Subtotal: ${result.subtotal:,.2f}",
            "",
            "Precio final sugerido:",
            f"${result.final_price:,.2f}",
        ]

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\n".join(lines))
        self.result_text.configure(state="disabled")

    def clear_form(self) -> None:
        self.quantity_var.set("")
        self.width_var.set("")
        self.height_var.set("")
        self.material_var.set("MDF 3 mm")
        self.work_type_var.set("Corte")
        self.complexity_var.set("Baja")
        self.coverage_var.set("Baja")

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.configure(state="disabled")


def main() -> None:
    root = tk.Tk()
    app = VectoraCotizadorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
