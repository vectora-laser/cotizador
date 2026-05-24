# Vectora Cotizador

Aplicación de escritorio en **Python + Tkinter** para presupuestar trabajos de corte y grabado láser de forma rápida.

## Ejecutar

```bash
python main.py
```

## Estructura

- `main.py`: interfaz gráfica y validaciones de entrada.
- `calculator.py`: lógica de cálculo desacoplada de la UI.
- `config.py`: parámetros configurables de negocio.

## Fórmula implementada

- Área: `ancho * alto`
- Costo material: `area * precio_cm2 * cantidad`
- Costo corte: `area * factor_complejidad * tarifa_corte * cantidad` (si aplica)
- Costo grabado: `area * factor_cobertura * tarifa_grabado * cantidad` (si aplica)
- Subtotal: `material + corte + grabado + costo_fijo`
- Precio final: `subtotal * margen`

## Ajustes de negocio rápidos

Todos los importes y factores están en `CONFIG` dentro de `config.py`.

## Preparado para evolución

El código deja aislados los componentes para agregar más adelante:

- historial de presupuestos
- exportación a PDF
- API para migración a web/PWA

## Recomendación implementable (siguiente paso)

Tu sugerencia es excelente: agregar una pantalla de **Configuración** para editar precios y factores sin tocar código.

Propuesta técnica para la próxima iteración:

1. Persistir `CONFIG` en un archivo `settings.json`.
2. Cargar configuración al iniciar la app.
3. Crear ventana de configuración con validación y botón Guardar.
4. Reusar `calculator.py` sin cambios.

Con eso el negocio puede ajustar precios en minutos.
