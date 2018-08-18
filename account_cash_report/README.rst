=============================
Reporte diario de facturacion
=============================

Este reporte se encuentra en Contabilidad / Cajas / Reporte de facturacion

El reporte de facturacion esta personalizado para cada caja, y muestra todas
las que fueron validadas en el periodo y el total acumulado en cada medio
de pago, agregando un medio de pago ficticio llamado **Cuenta Corriente** el
cual acumula el monto adeudado de todas las facturas listadas.

El filtro del reporte tiene los siguientes campos:

**Fecha Inicial** y **Fecha Final** Rango de fechas sobre el cual se genera el
reporte, en general la fecha inicial y final coinciden.

**Caja**: Es la caja para la cual se genera el reporte

Facturas
--------

Se listan todas las facturas validadas por el usuario de la caja que se
seleccionó en el filtro. Las cuales representan razonablemente las ventas
del periodo.
Estos son las columnas del listado:

**Nro de Factura** Es en numero de la factura que se compone del tipo de factura
FA-A, FA-B, NC-A, NC-B, ND-A, ND-B el punto de venta (4 digitos) y el numero de
comprobante (8 digitos). Por ejemplo FA-A 0001-00000054

**Total** Valor total de la factura con impuestos.

**Diario** Es el diario que se usa como medio de pago para recibir el pago de
la factura, son todos los medios de pago habilitados para la caja, pero también
pueden ser otros por ejemplo:

*RETENCIONES SUFRIDAS*, si la factura se pagó en parte con una retención,

*Ventas 01* Si es una nota de credito que cancela una factura, ambas se pagan
con el diario de facturacion. Se pueden dar casos mas complejos en donde se hace
una nota de credito parcial y se paga el resto con algun medio de pago.

*Cuenta corriente* si parte o toda la factura no esta cancelada se acumula en
este concepto que no es un diario, ni un medio de pago.

Por ultimo la factura puede tener varios pagos con distintos medios de pago, en
ese caso se listan todos los diarios separados por coma.

**Cliente** El cliente que aparece en la factura

**Vendedor** El vendedor que genero la venta

Debajo de todas las facturas se encuentra el **Total Facturado** que es la suma
de los totales de cada factura.

Medios de pago y cuenta corriente
---------------------------------
Los medios de pago representan exactamente (salvo cuentas corrientes) el dinero
ingresado por la caja.

Son los medios de pago que la cajera usa para cobrar las facturas, con el total
procesado en cada uno, mas un medio de pago ficticio llamado Cuenta corriente
que no esta cancelando facturas sino que se calcula como la suma de los saldos
no cancelados de todas las facturas listadas.


Debajo de los diarios se encuentra un totalizador que suma el total de cada
medio de pago mas el de las cuentas corrientes.

NOTA: Tener en cuenta que el total en Cuenta Corriente depende de la fecha en
la que se genera el reporte, por ejemplo si se genera un reporte en un periodo
anterior puede ser que el monto adeudado se haya saldado y la cuenta corriente
queden en cero.

NOTA: Tener en cuenta que el medio de pago Efectivo Ventas responde a las
transferencias que se hacen de Efectivo Ventas a Efectivo con lo cual si esa
transferencia no se hizo correctamente el total de este medio de pago no sera
correcto.

NOTA: Tener en cuenta que el total Facturado en general no coincidira con el
balance de los diarios por varias razones, por ejemplo:
- Se valida una nota de credito que cancela una factura con fecha fuera del
periodo analizado.
- Se cobran facturas que se validaron en fechas fuera del periodo.
- Una factura que en parte se paga con una retencion.

NOTA: En caso de dudas ver el reporte de cajas con apertura para determinar que
movimientos componen el total de cada medio de pago.

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
