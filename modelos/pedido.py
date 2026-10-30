from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pedido:
    id: str
    cliente: object
    estado: str
    dias: int
    items: tuple = field(default_factory=tuple)
