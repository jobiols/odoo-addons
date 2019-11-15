Este modulo esta inspirado en product_price_update_sale

Con las siguientes mejoras

1. Quitamos la dependencia de stock, solo depende de producto y Gestion de ventas.
2. Se puede filtrar por multiples categorias
3. Se puede filtrar por multiples proveedores
4. La actualizacion se hace por SQL y es ridiculamente rapida.

Permite hacer una actualizacion masiva de precios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Se selecciona un conjunto de productos**

- Por un conjunto de categorias
- Por un conjunto de proveedores
- Por mascara de referencia interna

**Se determina que precio se va a actualizar**

- Actualizar precio de venta en formulario de producto
- Actualizar precio de costo en formulario de producto
- Actualizar precio de costo del proveedor. En este caso lo que se actualiza es el precio que aparece en la pestana Compras en la linea correspondiente al proveedor. Este es el precio que el sistema toma al hacer una orden de compra.

**Se determina una forma de actualizacion**

- Incremento o decremento del precio por porcentaje
- Incremento o decremento del precio en valor absoluto

Se provee un boton **Chequear** para visualizar los productos que van a ser
afectados por la actualizacion. Este boton se provee a modo de verificacion
pero no es necesario chequear antes de aplicar la actualizacion.

NOTAS:

- No funciona en multimoneda ni multicompañia.
- Para trabajar con precio de proveedor se supone que hay solo un proveedor por producto y que no se usan las fechas de validez.
- No tiene seguridad, cualquiera puede modificar precios.
