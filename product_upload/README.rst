.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Carga / Actualizacion de productos por planilla
===============================================

Este modulo crea/actualiza productos desde una planilla excel. Cada hoja de la
planilla agrupa productos de un determinado proveedor y la referencia del
proveedor (que se encuentra en la ficha del proveedor bajo su nombre) debe ser
el nombre de la hoja.

Installation
============

 openpyxl required,
 install with: pip install openpyxl

Configuration
=============

 The user must have Inventory Manager rights.

Usage
=====

Ir a Inventario / Control de Inventario / Importar productos

Crear y subir una planilla con los productos a Crear / Actualizar

Columnas de la planilla:

- **Referencia Interna**
- **Precio de costo sin iva**
- **Moneda** es la moneda en la que se interpreta el costo (ARS,USD, etc...), si no esta activada la opcion multimoneda esta columna se ignora.
- **Margen** es el margen en porcentaje entre costo y precio de venta, el precio de venta se calculara como costo * (1+margen) por ejemplo 30%
- **Descripcion** Es la descripcion del producto
- **Codigo de barras**
- **Codigo de publicacion mercadolibre** Codigo alfanumerico para la publicacion
- **Publicado en mercadoshops** 1=Si 0=No
- **IVA Compras** Porcentaje de iva para las compras ejemplo 21%
- **IVA Ventas** Porcentaje de iva par las ventas ejemplo 10.5%

Si la referencia interna existe en la base de datos se actualizan los datos, si no existe se crean

**Campos requeridos para actualizacion**

- Referencia interna
- Precio de costo sin iva
- Moneda
- Margen

**Campos requeridos para creacion**

- Referencia interna
- Precio de costo sin iva
- Moneda
- Margen
- Descripcion
- IVA Compras
- IVA Ventas

**Por defecto se cargan los siguientes campos**

- Puede ser vendido: Si
- Puede ser comprado: Si
- Tipo de producto: Producto almacenable
- Politica de facturacion: Cantidades pedidas
- Control facturas de compra: Sobre cantidades pedidas
- Rutas: Comprar
- Garantia: 0 meses
- Plazo de entrega al cliente: 0 dias

