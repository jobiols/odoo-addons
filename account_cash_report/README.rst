=============================
Reporte diario de facturacion
=============================

Este reporte se encuentra en Contabilidad / Cajas / Reporte de facturacion

El reporte de facturacion esta personalizado para cada caja, y muestra las
facturase que fueron validadas en esta caja y el total acumulado en cada medio
de pago, agregando un medio de pago ficticio llamado **Cuenta Corriente** el
cual acumula el total de las facturas impagas.

Facturas
--------

Se listan todas las facturas validadas por el usuario de la caja que se seleccionó
en el filtro. Estos son las columnas del listado:

**Nro de Factura** Es en numero de la factura que se compone del tipo de factura
FA-A, FA-B, NC-A, NC-B, ND-A, ND-B el punto de venta (4 digitos) y el numero de
comprobante (8 digitos). Por ejemplo FA-A 0001-00000054

**Diario** Es el diario que se usa como medio de pago para recibir el pago de
la factura, son todos los medios de pago habilitados para la caja, pero también
pueden ser otros por ejemplo:

*RETENCIONES SUFRIDAS*, si la factura se pagó en parte con una retención,

*Ventas 01* si es una nota de credito que cancela una factura en ese caso se
esta pagando con la factura.

*Cuenta corriente* si parte o toda la factura no esta cancelada.

Por ultimo la factura puede tener varios pagos con distintos medios de pago, en
ese caso se listan todos los diarios separados por coma.

**Cliente** El cliente que aparece en la factura

**Vendedor** El vendedor que genero la venta


Diarios involucrados
--------------------
Son todos los diarios que estan involucrados en la cancelacion de las facturas
listadas anteriormente. Mas un diario ficticio llamado Cuenta corriente que no
esta cancelando facturas sino que se calcula como la suma de los saldos no
cancelados de todas las facturas listadas.


===================================
Reporte diario para cierre de cajas
===================================

Este reporte se encuentra en Contabilidad / Cajas / Reporte de cajas

El reporte de cajas esta personalizado para cada caja, y muestra el saldo total
registrado en cada medio de pago, para la fecha o rango de fechas seleccionado.

El filtro del reporte tiene los siguientes campos:

**Fecha Inicial** y **Fecha Final** Rango de fechas sobre el cual se genera el
reporte, en general la fecha inicial y final coinciden.

**Caja**: Es la caja para la cual se genera el reporte

**Expandir movimientos** Si se tilda expandir movimientos, se muestran todos los
movimientos que componen el saldo de cada medio de pago.

Definicion de caja
------------------
Una caja es un conjunto de medios de pago que se puede asignar a una cajera,
cuando la cajera selecciona el medio de pago se le muestran solo los que
estan definidos en su caja.

Medios de pago
--------------
Los medios de pago estan representados por diarios, a los cuales se les
agregan los campos:

**Caja**: Seleccion de la caja a la que pertenece el diario. Puede no pertenecer
a ninguna caja, en ese caso ninguna cajera lo puede usar.

**Genera Balance Inicial**: Si se tilda esta opcion en el reporte de cajas
se agregara un primer movimiento llamado balance inicial que representa el
dinero que hay en la caja al cierre del dia anterior.

**NOTA**: Tildando los diarios que representan efectivo (billetes) con este
ultimo campo se podra dejar en caja una cantidad de efectivo para iniciar el
dia siguiente el cual se sumara al total en el movimiento de Balance Inicial.
En los diarios que representan Tarjetas o Banco, no es necesario hacerlo ya
que siempre se rinde la totalidad del dinero.
