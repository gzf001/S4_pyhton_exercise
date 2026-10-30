from config import DIAS_PREFERENTE, DIAS_REGULAR, ESTADOS_ABIERTOS, UMBRAL_MONTO


def monto(pedido):
    return sum(item.subtotal for item in pedido.items)


def es_abierto(pedido):
    return pedido.estado in ESTADOS_ABIERTOS


def es_prioritario(pedido):
    limite_dias = DIAS_PREFERENTE if pedido.cliente.es_preferente() else DIAS_REGULAR
    return monto(pedido) >= UMBRAL_MONTO or pedido.dias >= limite_dias
