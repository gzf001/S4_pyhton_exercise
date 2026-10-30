from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    nombre: str
    tipo: str

    def es_preferente(self):
        return self.tipo == "preferente"
