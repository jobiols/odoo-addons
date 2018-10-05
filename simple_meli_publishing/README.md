Simple Meli Publishing
----------------------

Module para actualizar los precios de Mercadolibre con una planilla de calculo

Para actualizar los precios publicados en mercadolibre con planilla
excel se deberan cargar en los productos el codigo de publicacion, eso
aparece en la solapa Ventas de la ficha de producto.

Una vez cargado se sube la planilla que bajamos de mercadolibre con los
productos a odoo desde Ventas / procesar precios mercadolibre.

Al bajar nuevamente la planilla desde odoo los precios estaran 
actualizados al precio de lista mas iva y el stock sera el forecasting

Finalmente se vuelve a subir la planilla a Mercadolibre.

Se chequean los siguientes errores:
- El codigo de producto MLA no existe en odoo
- Odoo no deja cargar codigos de producto MLA repetidos
