# Sistema de pedidos

## Propósito

Procesa un conjunto de pedidos (archivo `pedidos.json`) y reporta, para los
pedidos **abiertos** (`pendiente` o `en_preparacion`):

- cuántos hay y cuál es el monto total,
- el monto abierto agrupado por tipo de cliente,
- cuántos son **prioritarios** (monto alto o demasiados días de espera),
- cuáles deben atenderse primero.

## Requisitos

- Python 3.9 o superior (usa `dataclasses` y f-strings).
- [pytest](https://docs.pytest.org/) para ejecutar las pruebas: `pip install pytest`.

No hay otras dependencias externas.

## Cómo ejecutar

```
python main.py
```

Lee `pedidos.json` (en la raíz del proyecto) e imprime el reporte en pantalla.

## Cómo ejecutar las pruebas

```
python -m pytest -v
```

## Responsabilidad de cada módulo

| Módulo | Responsabilidad |
|---|---|
| `config.py` | Única fuente de las constantes de negocio: `UMBRAL_MONTO`, `DIAS_REGULAR`, `DIAS_PREFERENTE`, `ESTADOS_ABIERTOS`. |
| `modelos/item.py` | `Item`: registro inmutable de una línea de pedido (nombre, cantidad, precio) y su subtotal. |
| `modelos/cliente.py` | `Cliente`: registro inmutable de un cliente (nombre, tipo) y si es preferente. |
| `modelos/pedido.py` | `Pedido`: registro inmutable de un pedido (id, cliente, estado, días, items). No tiene lógica de negocio. |
| `servicios/reglas.py` | Reglas de negocio puras: `monto`, `es_abierto`, `es_prioritario` (y `crear_regla_prioridad`, la fábrica que la construye). Reciben un `Pedido` y retornan un valor; no imprimen ni modifican nada. |
| `servicios/gestor_pedidos.py` | `GestorPedidos`: construye los `Pedido` a partir de datos ya leídos (`cargar`) y calcula los agregados —abiertos, monto, monto por tipo, prioritarios— aplicando las reglas de `reglas.py` (`procesar`). Es el único lugar con estado mutable. |
| `servicios/reporte.py` | `Reporte`: a partir de un `GestorPedidos`, construye la lista "Atender primero" y el texto completo del reporte (`formato`). No imprime. |
| `main.py` | Único punto de I/O y de `print`: lee `pedidos.json` y muestra el reporte. |
| `tests/` | Pruebas de las reglas de negocio (`test_reglas.py`) y fixtures compartidas (`conftest.py`). |

## Correcciones y robustecimientos (cambios de comportamiento)

Estos puntos **no son refactorización**: son defectos del comportamiento
original que se corrigieron, detectados y verificados con pruebas.

1. **Estado compartido entre instancias de `GestorPedidos`.**
   Los atributos (`pedidos`, `abiertos`, `monto`, `prioritarios`, `por_tipo`)
   estaban definidos a nivel de clase, por lo que todas las instancias
   compartían el mismo estado: un segundo `GestorPedidos` heredaba los
   pedidos y totales del primero. Se corrigió definiéndolos en `__init__`
   como atributos de instancia.
   Prueba que lo revela: `test_dos_gestores_independientes`.

2. **La lista "Atender primero" ignoraba el límite de días de los clientes preferentes.**
   El reporte usaba un límite fijo de 5 días para decidir si un pedido entra
   en "Atender primero", sin aplicar el límite de 3 días que corresponde a
   clientes preferentes (esa distinción sí existía al contar prioritarios,
   pero no al armar la lista). Resultado: un pedido preferente con 3 días
   podía contarse como prioritario y nunca aparecer en la lista. Se corrigió
   unificando ambos cálculos en una sola regla (`reglas.es_prioritario`).
   Prueba que lo revela: `test_limite_de_dias_preferente`.

3. **El empate en días se desempataba en el orden incorrecto.**
   Al ordenar "Atender primero" por `(días, id)` con `reverse=True`, el
   `reverse` invertía también el `id`: ante un empate en días, los pedidos
   quedaban en orden descendente por id en vez de ascendente. Se corrigió
   ordenando por `(-días, id)` sin invertir la tupla completa.
   Prueba que lo revela: `test_empate_en_dias`.
