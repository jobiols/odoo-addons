.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
  :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
  :alt: License: AGPL-3

====================
Product Currency Fix
====================

Corrige un problema en Product Currency, vale en estas condiciones

- Hay productos con precio / costo en una currency distinta a la de la compania usando el modulo Product Currency
- En inventario / contabilidad esta definido Valoracion de inventario perpetuo
- En las categorias esta definido Metodo costo Precio real, Valoracion inventario Perpetuo, Forzar estrategia FIFO

En estas condiciones en odoo standard, cuando se valida una orden de compra,
se crea un stock.move con el costo del producto para luego ponerlo en el
stock.quant traduciendolo a la moneda de la compania.
Al vender el producto, copia el costo del quant mas antiguo (FIFO) al costo
del producto.

El problema es que al copiar de vuelta el costo al producto lo pone en la moneda
de la compania cuando deberia ponerlo en la moneda del producto.

Que hace el fix:

Define un nuevo costo como standard_product_cost y muestra eso en la ficha del
producto y en el product tree.

Define un precio unitario como price_product_unit que esta en stock.move para
guardar el historico del costo del producto en la moneda del producto