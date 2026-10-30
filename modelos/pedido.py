from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pedido:
    """Registro inmutable de un pedido.

    `dias` son los días que el pedido lleva sin completarse (usados por
    servicios.reglas para decidir si es prioritario). `items` es una tupla
    de Item, no una lista: un Pedido no se modifica después de creado.
    """
    id: str
    cliente: object
    estado: str
    dias: int
    items: tuple = field(default_factory=tuple)
