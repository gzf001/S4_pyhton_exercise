from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    nombre: str
    cantidad: int
    precio: int

    @property
    def subtotal(self):
        return self.cantidad * self.precio
