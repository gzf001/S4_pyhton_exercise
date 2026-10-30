from servicios import reglas


class Reporte:
    def __init__(self, gestor):
        self.gestor = gestor

    def lista_atencion(self):
        abiertos = filter(reglas.es_abierto, self.gestor.pedidos)
        prioritarios = filter(reglas.es_prioritario, abiertos)
        return sorted(prioritarios, key=lambda p: (-p.dias, p.id))

    # construye el texto del reporte; no imprime ni hace I/O
    def formato(self):
        atencion = self.lista_atencion()
        lineas = [f"  [!] Pedido {p.id} es prioritario" for p in atencion]
        lineas.append("===== REPORTE DE PEDIDOS =====")
        lineas.append(f"Pedidos abiertos: {self.gestor.abiertos}")
        lineas.append(f"Monto abierto: {self.gestor.monto}")
        lineas.append(f"Pedidos prioritarios: {self.gestor.prioritarios}")
        lineas.append(f"Atender primero: {[p.id for p in atencion]}")
        for t in self.gestor.por_tipo:
            lineas.append(f"Monto {t}: {self.gestor.por_tipo[t]}")
        return "\n".join(lineas)
