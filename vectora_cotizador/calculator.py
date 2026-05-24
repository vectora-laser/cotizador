"""Lógica de negocio para cotizaciones de Vectora Cotizador.

Se mantiene aislada de la interfaz para facilitar pruebas, mantenimiento
y migración futura a PWA o API.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class QuoteInput:
    """Datos de entrada para un presupuesto."""

    material: str
    work_type: str
    quantity: int
    width_cm: float
    height_cm: float
    cut_complexity: str
    engraving_coverage: str


@dataclass(frozen=True)
class QuoteResult:
    """Resultado detallado del cálculo."""

    area_total: float
    material_cost: float
    cut_cost: float
    engraving_cost: float
    fixed_cost: float
    subtotal: float
    final_price: float


def _includes_cut(work_type: str) -> bool:
    return "Corte" in work_type


def _includes_engraving(work_type: str) -> bool:
    return "Grabado" in work_type


def calculate_quote(data: QuoteInput, config: Dict[str, Any]) -> QuoteResult:
    """Calcula un presupuesto con base en la configuración indicada."""

    material_cfg = config["materiales"][data.material]
    precio_cm2 = material_cfg["precio_cm2"]
    # Tarifas por material: reflejan tiempo aproximado real de máquina.
    tarifa_corte = material_cfg["tarifa_corte"]
    tarifa_grabado = material_cfg["tarifa_grabado"]

    factor_complejidad = config["factores_complejidad"][data.cut_complexity]
    factor_cobertura = config["factores_cobertura"][data.engraving_coverage]

    area = data.width_cm * data.height_cm
    area_total = area * data.quantity

    material_cost = area_total * precio_cm2

    cut_cost = 0.0
    if _includes_cut(data.work_type):
        cut_cost = (
            area
            * factor_complejidad
            * tarifa_corte
            * data.quantity
        )

    engraving_cost = 0.0
    if _includes_engraving(data.work_type):
        engraving_cost = (
            area
            * factor_cobertura
            * tarifa_grabado
            * data.quantity
        )

    fixed_cost = config["costo_fijo"]
    subtotal = material_cost + cut_cost + engraving_cost + fixed_cost
    final_price = subtotal * config["margen"]

    return QuoteResult(
        area_total=area_total,
        material_cost=material_cost,
        cut_cost=cut_cost,
        engraving_cost=engraving_cost,
        fixed_cost=fixed_cost,
        subtotal=subtotal,
        final_price=final_price,
    )
