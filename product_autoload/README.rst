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
- Códigos de barras (multiples codigos por producto)
- Precio de costo - Precio al que la ferretería minorista compra el producto sin iva
- UPV Agrupacion mayorista
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

Armado de Categorias
--------------------

Por el momento y a falta de conocimiento de los datos las categorias quedaron
armadas de la siguiente forma:

Para cada producto la categoria se arma de la siguiente forma:

- Obtengo el codigo de item correspondiente al producto, que se define por los
digitos del codigo del producto hasta el primer punto.
- Con el codigo de item obtengo el item, familia y seccion
- del item obtengo la familia
- Armo la categoria con Nombre de seccion / Nombre de familia / Nombre de item

