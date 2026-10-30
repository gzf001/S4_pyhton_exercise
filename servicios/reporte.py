from servicios import reglas


class Reporte:
    def __init__(self, gestor):
        self.gestor = gestor

    def lista_atencion(self):
        abiertos = [p for p in self.gestor.pedidos if reglas.es_abierto(p)]
        prioritarios = [p for p in abiertos if reglas.es_prioritario(p)]
        return sorted(prioritarios, key=lambda p: (-p.dias, p.id))

    def imprimir(self):
        print("===== REPORTE DE PEDIDOS =====")
        print("Pedidos abiertos:", self.gestor.abiertos)
        print("Monto abierto:", self.gestor.monto)
        print("Pedidos prioritarios:", self.gestor.prioritarios)
        print("Atender primero:", [p.id for p in self.lista_atencion()])
        for t in self.gestor.por_tipo:
            print("Monto", t + ":", self.gestor.por_tipo[t])
