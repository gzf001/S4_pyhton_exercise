"""Orquesta la carga y el procesamiento de pedidos.

A diferencia de modelos/ y servicios/reglas.py, esta clase sí mantiene estado
(los atributos calculados tras llamar a procesar()); por eso concentra aquí
los únicos cálculos con efecto sobre `self`, delegando toda regla de negocio
a servicios/reglas.py.
"""

from functools import reduce

from modelos.cliente import Cliente
from modelos.item import Item
from modelos.pedido import Pedido
from servicios import reglas


def _acumular_monto_por_tipo(acumulado, pedido):
    """Callback de reduce: retorna un dict NUEVO (no muta `acumulado`)."""
    tipo = pedido.cliente.tipo
    return {**acumulado, tipo: acumulado.get(tipo, 0) + reglas.monto(pedido)}


class GestorPedidos:
    def __init__(self):
        self.pedidos = []
        self.abiertos = 0
        self.monto = 0
        self.prioritarios = 0
        self.por_tipo = {}

    def cargar(self, datos):
        """Construye los Pedido a partir de datos ya leídos (no hace I/O).

        `datos` es una lista de dicts con la forma del JSON de pedidos
        (id, cliente, tipo, estado, dias, items). Cada entrada que no tenga
        esa forma se descarta en silencio: un registro malformado no
        interrumpe la carga del resto.
        """
        for d in datos:
            try:
                items = tuple(Item(it[0], it[1], it[2]) for it in d["items"])
                p = Pedido(d["id"], Cliente(d["cliente"], d["tipo"]), d["estado"], d["dias"], items)
                self.pedidos.append(p)
            except:
                pass

    def procesar(self):
        """Calcula los agregados sobre self.pedidos y los guarda en self.

        Requiere haber llamado antes a cargar(). `prioritarios` cuenta solo
        los pedidos que además están abiertos (un pedido prioritario pero ya
        despachado no se contabiliza).
        """
        abiertos = list(filter(reglas.es_abierto, self.pedidos))
        self.abiertos = len(abiertos)
        self.monto = sum(map(reglas.monto, abiertos))
        self.por_tipo = reduce(_acumular_monto_por_tipo, abiertos, {})

        self.prioritarios = len(list(filter(reglas.es_prioritario, abiertos)))

    def calcular_descuento(self, p, porcentaje):
        """Retorna el descuento sobre el monto de `p` para `porcentaje` (0-100)."""
        return reglas.monto(p) * porcentaje / 100
