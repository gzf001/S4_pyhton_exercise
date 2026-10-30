"""Formatea el estado de un GestorPedidos como texto. No hace I/O."""

from servicios import reglas


class Reporte:
    def __init__(self, gestor):
        self.gestor = gestor

    def lista_atencion(self):
        """Pedidos abiertos y prioritarios, listos para "Atender primero".

        Orden: más días de espera primero; en caso de empate, por id
        ascendente.
        """
        abiertos = filter(reglas.es_abierto, self.gestor.pedidos)
        prioritarios = filter(reglas.es_prioritario, abiertos)
        return sorted(prioritarios, key=lambda p: (-p.dias, p.id))

    def formato(self):
        """Retorna el texto completo del reporte (no imprime ni hace I/O)."""
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
