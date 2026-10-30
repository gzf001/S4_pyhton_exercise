from config import DIAS_PREFERENTE, DIAS_REGULAR, ESTADOS_ABIERTOS, UMBRAL_MONTO


def monto(pedido):
    return sum(item.subtotal for item in pedido.items)


def es_abierto(pedido):
    return pedido.estado in ESTADOS_ABIERTOS


def crear_regla_prioridad(umbral_monto, dias_regular, dias_preferente):
    def regla(pedido):
        limite_dias = dias_preferente if pedido.cliente.es_preferente() else dias_regular
        return monto(pedido) >= umbral_monto or pedido.dias >= limite_dias
    return regla


es_prioritario = crear_regla_prioridad(UMBRAL_MONTO, DIAS_REGULAR, DIAS_PREFERENTE)
