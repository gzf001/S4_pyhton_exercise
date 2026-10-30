"""Reglas de negocio puras: reciben un Pedido y retornan un valor.

No imprimen ni modifican nada (ni el pedido, ni variables externas), para
poder probarlas de forma aislada y para que exista un solo lugar donde cada
regla está definida.
"""

from config import DIAS_PREFERENTE, DIAS_REGULAR, ESTADOS_ABIERTOS, UMBRAL_MONTO


def monto(pedido):
    """Retorna la suma de los subtotales de los items del pedido."""
    return sum(item.subtotal for item in pedido.items)


def es_abierto(pedido):
    """Retorna True si el estado del pedido está en ESTADOS_ABIERTOS."""
    return pedido.estado in ESTADOS_ABIERTOS


def crear_regla_prioridad(umbral_monto, dias_regular, dias_preferente):
    """Construye la función que decide si un pedido es prioritario.

    Un pedido es prioritario si su monto es mayor o igual a `umbral_monto`,
    o si sus días de espera son mayores o iguales al límite correspondiente
    a su tipo de cliente (`dias_preferente` para clientes preferentes,
    `dias_regular` para el resto). Ambos límites son inclusivos (>=).

    Al recibir los umbrales como parámetros en vez de usar constantes fijas,
    se puede crear otra regla de prioridad (por ejemplo, para una temporada
    con umbrales distintos) sin tocar esta función.

    Retorna una función `(pedido) -> bool`.
    """
    def regla(pedido):
        limite_dias = dias_preferente if pedido.cliente.es_preferente() else dias_regular
        return monto(pedido) >= umbral_monto or pedido.dias >= limite_dias
    return regla


# Regla de prioridad vigente del negocio, construida con los umbrales de config.py.
es_prioritario = crear_regla_prioridad(UMBRAL_MONTO, DIAS_REGULAR, DIAS_PREFERENTE)
