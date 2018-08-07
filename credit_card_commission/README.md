
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Credit Card Commission Calculator
=================================

Este módulo calcula el recargo de una tarjeta de crédito en base a las cuotas que elige el cliente.

Agrega en configuración un menu para poner los coeficientes de las tarjetas según las cuotas

Agrega en el producto un tipo de producto recargo_tarjeta, si en un producto se elige recargo tarjeta aparece
un formulario que permite elegir

La marca de la tarjeta

La cantidad de cuotas de una lista.


 nro cuotas | recargo | total | valor cuota |
 -----------|---------|-------|-------------|
 2|50|1500|66|


Cuando se tiene una factura o presupuesto, se selecciona este producto y se edita, el producto explora la
factura y se trae el precio final con iva para calcular las tablas.

Se carga como un producto y en el tipo de producto se pone tarjeta de crédito.
Entonces el form cambia y permite elegir la tarjeta y el numero de cuotas.
Tiene que hacer un correccion para incluir la comision en el precio al calcular la cuota

Cuando se salva trae al presupuesto o a la factura con el recargo.
