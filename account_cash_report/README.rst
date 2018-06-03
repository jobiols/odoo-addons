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
