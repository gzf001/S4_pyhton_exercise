import json
import os

import pytest

from servicios.gestor_pedidos import GestorPedidos
from servicios.reporte import Reporte

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def pedido(id, tipo, estado, dias, monto):
    return {"id": id, "cliente": "Cliente " + id, "tipo": tipo, "estado": estado,
            "dias": dias, "items": [["Producto", 1, monto]]}

def ejecutar(ruta):
    g = GestorPedidos()
    g.cargar(ruta)
    g.procesar()
    r = Reporte(g)
    return {
        "abiertos": g.abiertos,
        "monto": g.monto,
        "prioritarios": g.prioritarios,
        "atencion": [p.id for p in r.lista_atencion()],
        "por_tipo": dict(g.por_tipo),
    }


def es_prioritario(res, id):
    return res["prioritarios"] == 1 and res["atencion"] == [id]


def no_es_prioritario(res):
    return res["prioritarios"] == 0 and res["atencion"] == []


# Esperado: 5 abiertos · $521.820 · 3 prioritarios · [P-202, P-204, P-205]
def test_habitual(archivo_json):
    with open(os.path.join(RAIZ, "pedidos.json"), encoding="utf-8") as f:
        datos = json.load(f)
    res = ejecutar(archivo_json(datos))
    assert res["abiertos"] == 5
    assert res["monto"] == 521820
    assert res["prioritarios"] == 3
    assert res["atencion"] == ["P-202", "P-204", "P-205"]


# Esperado: prioritario (monto exactamente en el umbral)
def test_limite_de_monto(archivo_json):
    res = ejecutar(archivo_json([pedido("P-1", "regular", "pendiente", 1, 150000)]))
    assert es_prioritario(res, "P-1")


# Esperado: no prioritario
def test_bajo_el_limite_de_monto(archivo_json):
    res = ejecutar(archivo_json([pedido("P-1", "regular", "pendiente", 4, 149999)]))
    assert no_es_prioritario(res)


# Esperado: prioritario (regular, 5 días)
def test_limite_de_dias_regular(archivo_json):
    res = ejecutar(archivo_json([pedido("P-1", "regular", "pendiente", 5, 40000)]))
    assert es_prioritario(res, "P-1")


# Esperado: prioritario y presente en "Atender primero" (preferente, 3 días)
def test_limite_de_dias_preferente(archivo_json):
    res = ejecutar(archivo_json([pedido("P-1", "preferente", "pendiente", 3, 40000)]))
    assert res["prioritarios"] == 1
    assert res["atencion"] == ["P-1"]


# Esperado: no prioritario (preferente, 2 días)
def test_bajo_el_limite_preferente(archivo_json):
    res = ejecutar(archivo_json([pedido("P-1", "preferente", "pendiente", 2, 40000)]))
    assert no_es_prioritario(res)


# Esperado: 0 · $0 · 0 · []
def test_no_abiertos(archivo_json):
    res = ejecutar(archivo_json([
        pedido("P-1", "regular", "despachado", 9, 300000),
        pedido("P-2", "preferente", "cancelado", 9, 300000),
    ]))
    assert (res["abiertos"], res["monto"], res["prioritarios"], res["atencion"]) == (0, 0, 0, [])


# Esperado: 0 · $0 · 0 · []
def test_coleccion_vacia(archivo_json):
    res = ejecutar(archivo_json([]))
    assert (res["abiertos"], res["monto"], res["prioritarios"], res["atencion"]) == (0, 0, 0, [])


# Esperado: [P-300, P-301] (empate en días se desempata por id ascendente)
def test_empate_en_dias(archivo_json):
    res = ejecutar(archivo_json([
        pedido("P-300", "regular", "pendiente", 5, 40000),
        pedido("P-301", "regular", "pendiente", 5, 40000),
    ]))
    assert res["atencion"] == ["P-300", "P-301"]


# Caso propio 1 - Esperado: cada gestor 1 abierto . $40.000 . 0 prioritarios . []
def test_dos_gestores_independientes(archivo_json):
    ruta = archivo_json([pedido("P-1", "regular", "pendiente", 1, 40000)])
    primero = ejecutar(ruta)
    segundo = ejecutar(ruta)
    for res in (primero, segundo):
        assert (res["abiertos"], res["monto"], res["prioritarios"], res["atencion"]) == (1, 40000, 0, [])


# Caso propio 2 - Esperado: 2 abiertos - $100.000 - regular $40.000 - preferente $60.000
def test_montos_por_tipo(archivo_json):
    res = ejecutar(archivo_json([
        pedido("P-1", "regular", "pendiente", 1, 40000),
        pedido("P-2", "preferente", "en_preparacion", 1, 60000),
        pedido("P-3", "regular", "despachado", 1, 100000),
    ]))
    assert res["abiertos"] == 2
    assert res["monto"] == 100000
    assert res["por_tipo"] == {"regular": 40000, "preferente": 60000}
