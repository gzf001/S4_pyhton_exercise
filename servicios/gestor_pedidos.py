from functools import reduce

from modelos.cliente import Cliente
from modelos.item import Item
from modelos.pedido import Pedido
from servicios import reglas


def _acumular_monto_por_tipo(acumulado, pedido):
    tipo = pedido.cliente.tipo
    return {**acumulado, tipo: acumulado.get(tipo, 0) + reglas.monto(pedido)}


class GestorPedidos:
    def __init__(self):
        self.pedidos = []
        self.abiertos = 0
        self.monto = 0
        self.prioritarios = 0
        self.por_tipo = {}

    # construye los pedidos a partir de datos ya leídos (la lectura de archivo
    # ocurre en main.py; esta función no hace I/O)
    def cargar(self, datos):
        for d in datos:
            try:
                items = tuple(Item(it[0], it[1], it[2]) for it in d["items"])
                p = Pedido(d["id"], Cliente(d["cliente"], d["tipo"]), d["estado"], d["dias"], items)
                self.pedidos.append(p)
            except:
                pass

    # procesa los pedidos
    def procesar(self):
        abiertos = list(filter(reglas.es_abierto, self.pedidos))
        self.abiertos = len(abiertos)
        self.monto = sum(map(reglas.monto, abiertos))
        self.por_tipo = reduce(_acumular_monto_por_tipo, abiertos, {})

        self.prioritarios = len(list(filter(reglas.es_prioritario, abiertos)))

    def calcular_descuento(self, p, porcentaje):
        return reglas.monto(p) * porcentaje / 100
