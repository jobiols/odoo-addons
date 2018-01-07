Customización mayorista de ceramicas
====================================

- Parametro adicional m2 o m por caja en producto
- Si se usan descuentos, el Comercial solo pueden poner descuentos hasta 10%
- Listas de precios restringidas, solo las ven Administrador y Encargado
- Definicion de remitos para envios o para retiro en sucursal
- Definicion de tres columnas configurables en listado de productos para
mostrar listas de precio.
- Rutas para definir envios o retiros desde el presupuesto.

Definicion de cuatro grupos de usuarios
---------------------------------------
- Administrador
- Encargado
- Comercial
- Almacen

Se usan las restricciones de los stores
---------------------------------------
- Los usuarios de almacen tienen restrignidos los almacenes y diarios.
- Los usuarios comerciales tienen restringidos diarios.

Definicion de rutas
-------------------
Se requiere definir para cada almacen una ubicacion Envio y dos rutas, suponiendo un almacen WH las
rutas tendrian la siguiente forma:

**Ruta WH** genera un remito para que lo vengan a retirar al almacen

WH:Stock -> Ubicaciones Clientes

**Ruta WHE** genera un remito para que lo envien a la direccion de envio del cliente

WHE:Stock -> Envios (Método de abastecimiento = Obtener de las existencias)

WHE:Envios -> Ubicaciones Clientes (Método de abastecimiento = crear abastecimiento)
