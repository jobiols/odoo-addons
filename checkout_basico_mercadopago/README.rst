.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Este modulo está en desarrollo y todavia no ha sido liberado

Checkout Básico Mercadopago
===========================
Implementa el checkout tal como se describe en la página de mercadopago
(https://www.mercadopago.com.ar/developers/es/solutions/payments/basic-checkout/receive-payments/)

Recibir pagos
-------------
En pagos de cliente si se elije un metodo de pago marcado como tarjeta al lado del
importe aparece el botón [Cobrar]. Oprimiendo cobrar lanza un popup con el sitio de
mercadopago y permite cobrar con tarjeta.

Utilizar mercadoenvios
----------------------
Si tiene activado mercadoenvios, en la orden de venta aparece un botón [Mercadoenvios]
en el producto debe estar definido el peso y las dimensiones para que se le transmitan
a mercadoenvios

Devoluciones y cancelaciones
----------------------------
No implementado

Recibir notificaciones de las operaciones
-----------------------------------------
No implementado
Requiere una url donde mercadopago postea las notificaciones.

