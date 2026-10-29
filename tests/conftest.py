import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servicios.gestor_pedidos import GestorPedidos

@pytest.fixture(autouse=True)
def gestor_limpio(monkeypatch):
    # GestorPedidos guarda su estado en atributos de clase (señal 3); se reinician
    # por prueba para que un caso no contamine al siguiente. No modifica el proyecto.
    monkeypatch.setattr(GestorPedidos, "pedidos", [])
    monkeypatch.setattr(GestorPedidos, "abiertos", 0)
    monkeypatch.setattr(GestorPedidos, "monto", 0)
    monkeypatch.setattr(GestorPedidos, "prioritarios", 0)
    monkeypatch.setattr(GestorPedidos, "por_tipo", {})

@pytest.fixture
def archivo_json(tmp_path):
    def crear(datos):
        ruta = tmp_path / "pedidos.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return str(ruta)
    return crear
