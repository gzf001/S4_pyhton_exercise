from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pedido:
    id: str
    cliente: object
    estado: str
    dias: int
    items: tuple = field(default_factory=tuple)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items)
