# Vectora Cotizador

Aplicación de escritorio en **Python + Tkinter** para presupuestar trabajos de corte y grabado láser de forma rápida.

## Ejecutar

```bash
python main.py
```

## Estructura

- `main.py`: interfaz gráfica y validaciones de entrada.
- `calculator.py`: lógica de cálculo desacoplada de la UI.
- `config.py`: carga, guardado y saneamiento de configuración.
- `config.json`: parámetros editables sin tocar código.

## Fórmula implementada

- Área: `ancho * alto`
- Costo material: `area * precio_cm2 * cantidad`
- Costo corte: `area * factor_complejidad * tarifa_corte_material * cantidad` (si aplica)
- Costo grabado: `area * factor_cobertura * tarifa_grabado_material * cantidad` (si aplica)
- Subtotal: `material + corte + grabado + costo_fijo`
- Precio final: `subtotal * margen`

## Configuración editable

`config.json` soporta por material:

- `precio_cm2`
- `tarifa_corte`
- `tarifa_grabado`

Además se mantienen `load_config()` y `save_config()` en `config.py` para la futura pantalla de configuración en UI.

## Preparado para evolución

El código deja aislados los componentes para agregar más adelante:

- historial de presupuestos
- exportación a PDF
- pantalla de configuración persistente
- API para migración a web/PWA
