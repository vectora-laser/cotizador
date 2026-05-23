"""Configuración central de Vectora Cotizador.

Este módulo concentra todos los valores de negocio para que puedan
ajustarse desde un solo lugar y, más adelante, persistirse desde una
pantalla de configuración.
"""

CONFIG = {
    "materiales": {
        "MDF 3 mm": {"precio_cm2": 0.85},
        "MDF 5 mm": {"precio_cm2": 1.25},
        "PU": {"precio_cm2": 1.10},
    },
    "factores_complejidad": {
        "Baja": 1.0,
        "Media": 1.5,
        "Alta": 2.5,
    },
    "factores_cobertura": {
        "Baja": 0.2,
        "Media": 0.5,
        "Alta": 0.9,
    },
    "tarifa_corte": 0.15,
    "tarifa_grabado": 0.10,
    "costo_fijo": 500.0,
    "margen": 1.5,
}

# Claves pensadas para evolución futura:
# - historial_presupuestos: almacenamiento de cotizaciones
# - exportacion_pdf: parámetros de layout y branding
# - configuracion_persistente: path de archivo json/toml
