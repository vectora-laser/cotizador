"""Configuración central y persistencia de parámetros de Vectora Cotizador.

Este módulo concentra los valores de negocio y agrega soporte de
carga/guardado en JSON para futura pantalla de configuración.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

CONFIG_FILE = Path(__file__).with_name("config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "materiales": {
        "MDF 3 mm": {
            "precio_cm2": 1.5,
            # Las tarifas modelan tiempo estimado de máquina por cm².
            "tarifa_corte": 2.0,
            "tarifa_grabado": 1.2,
        },
        "MDF 5 mm": {
            "precio_cm2": 2.3,
            # Materiales más gruesos suelen requerir más pasadas de corte.
            "tarifa_corte": 3.5,
            "tarifa_grabado": 1.4,
        },
        "PU": {
            "precio_cm2": 1.8,
            "tarifa_corte": 1.4,
            "tarifa_grabado": 1.8,
        },
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
    "costo_fijo": 500.0,
    "margen": 1.5,
}


def _sanitize_config(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Asegura que la configuración tenga la estructura esperada."""

    clean = deepcopy(DEFAULT_CONFIG)

    if not isinstance(raw, dict):
        return clean

    for material, defaults in clean["materiales"].items():
        incoming = raw.get("materiales", {}).get(material, {})
        if isinstance(incoming, dict):
            for field in ("precio_cm2", "tarifa_corte", "tarifa_grabado"):
                value = incoming.get(field, defaults[field])
                clean["materiales"][material][field] = float(value)

    for key in ("factores_complejidad", "factores_cobertura"):
        incoming_group = raw.get(key, {})
        if isinstance(incoming_group, dict):
            for factor_name, default_value in clean[key].items():
                clean[key][factor_name] = float(incoming_group.get(factor_name, default_value))

    clean["costo_fijo"] = float(raw.get("costo_fijo", clean["costo_fijo"]))
    clean["margen"] = float(raw.get("margen", clean["margen"]))
    return clean


def load_config() -> Dict[str, Any]:
    """Carga configuración desde config.json o devuelve defaults."""

    if not CONFIG_FILE.exists():
        return deepcopy(DEFAULT_CONFIG)

    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return deepcopy(DEFAULT_CONFIG)

    return _sanitize_config(data)


def save_config(config: Dict[str, Any]) -> None:
    """Guarda configuración en config.json para edición futura vía UI."""

    clean = _sanitize_config(config)
    CONFIG_FILE.write_text(
        json.dumps(clean, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


CONFIG = load_config()
