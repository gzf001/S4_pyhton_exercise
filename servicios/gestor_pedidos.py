import json
from modelos.cliente import Cliente
from modelos.item import Item
from modelos.pedido import Pedido


class GestorPedidos:
    def __init__(self):
        self.pedidos = []
        self.abiertos = 0
        self.monto = 0
        self.prioritarios = 0
        self.por_tipo = {}

    def cargar(self, archivo):
        f = open(archivo, encoding="utf-8")
        datos = json.load(f)
        for d in datos:
            try:
                items = tuple(Item(it[0], it[1], it[2]) for it in d["items"])
                p = Pedido(d["id"], Cliente(d["cliente"], d["tipo"]), d["estado"], d["dias"], items)
                self.pedidos.append(p)
            except:
                pass

    # procesa los pedidos
    def procesar(self):
        for p in self.pedidos:
            if p.estado == "pendiente" or p.estado == "en_preparacion":
                self.abiertos += 1
                self.monto += p.total
                if p.cliente.tipo in self.por_tipo:
                    self.por_tipo[p.cliente.tipo] += p.total
                else:
                    self.por_tipo[p.cliente.tipo] = p.total
                limite = 5
                if p.cliente.es_preferente():
                    limite = 3
                if p.total >= 150000 or p.dias >= limite:
                    self.prioritarios += 1
                    print("  [!] Pedido", p.id, "es prioritario")

    def calcular_descuento(self, p, porcentaje):
        return p.total * porcentaje / 100
