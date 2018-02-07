=============================
Carga automatica de productos
=============================

Este modulo carga los productos en forma automatica disparado por una tarea
cron desde un directorio del servidor.
Se requiere que el archivo data sea actualizado por medios externos en forma
periodica.

Formato de archivo CSV para carga de datos
------------------------------------------

- El archivo debe contener un producto por línea
- El archivo debe utilizar la codificación de caracteres UTF-8.
- Si deben conservarse espacios en blanco iniciales o finales para un valor individual, o si el texto tiene una o varias comas, todo el valor debe especificarse entre comillas.
- Los valores numéricos se especifican con punto decimal y sin carácter de separación por miles.
- El timestamp tendrá el formato AAAA-MM-DD HH:MM:SS completando con ceros a la izquierda, por ejemplo 2018-01-30 10:03:22

data.csv
--------

- Código del producto
- Nombre del producto
- Descripción del producto
- Código de barras
- Precio de lista	- Precio sugerido de venta al público sin iva
- Precio de costo - Precio al que la ferretería minorista compra el producto sin iva
- Peso bruto en kg
- Volumen cm3
- Nombre de la imagen
- Garantia (meses)
- IVA %
- idRubro
- Timestamp actualización

item.csv
--------

- item_code
- name
- origin
- section_code
- family_code

family.csv
----------
- family_code
- name

section.csv
-----------

- section_code
- name
