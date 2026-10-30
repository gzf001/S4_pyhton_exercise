import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def archivo_json(tmp_path):
    def crear(datos):
        ruta = tmp_path / "pedidos.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return str(ruta)
    return crear
