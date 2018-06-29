Simple Meli Publishing
----------------------

Module para actualizar los precios de Mercadolibre con una planilla de calculo

Para actualizar los precios publicados en mercadolibre con planilla
excel se deberan cargar en los productos el codigo de publicacion, eso
aparece en la solapa Ventas de la ficha de producto.

Una vez cargado se sube la planilla a odoo desde Ventas / procesar precios
mercadolibre.

Al bajar la planilla los precios estaran actualizados al precio de lista mas iva

Finalmente se sube la planilla a Mercadolibre.

Se chequean los siguientes errores:
- El codigo de producto no existe en odoo
- El sku de la planilla no coincide con la referencia interna de odoo
- Odoo no deja cargar codigos de producto repetidos
