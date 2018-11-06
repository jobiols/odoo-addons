.. |company| replace:: jeo Soft

.. |company_logo| image:: https://gist.github.com/jobiols/74e6d9b7c6291f00ef50dba8e68123a6/raw/fa43efd45f08a2455dd91db94c4a58fd5bd3d660/logo-jeo-150x68.jpg
   :alt: jeo Soft
   :target: https://www.jeosoft.com.ar

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===============================================
Carga / Actualizacion de productos por planilla
===============================================

.. image:: https://travis-ci.org/jobiols/cl-vhing.svg?branch=11.0
    :target: https://travis-ci.org/jobiols/cl-vhing

.. image:: https://api.codeclimate.com/v1/badges/3a3a1f98794659f59527/maintainability
   :target: https://codeclimate.com/github/jobiols/cl-vhing/maintainability
   :alt: Maintainability

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
- **Moneda** es la moneda en la que se interpreta el costo (ARS,USD, etc...), si no esta activada la opcion multimoneda esta columna se ignora.
- **Precio de costo sin iva**
- **Precio de venta sin iva**
- **Descripcion** Es la descripcion del producto
- **IVA Compras** Porcentaje de iva para las compras ejemplo 21%
- **IVA Ventas** Porcentaje de iva par las ventas ejemplo 10.5%
- **Codigo de barras**
- **Codigo de publicacion mercadolibre** Codigo alfanumerico para la publicacion
- **Parent** Codigo de producto del que copiara el precio

Si la referencia interna existe en la base de datos se actualizan los datos, si no existe se crean

**Campos requeridos para actualizacion**

- Referencia interna
- Moneda
- Precio de costo sin iva
- Precio de venta sin iva

**Campos requeridos para creacion**

- Referencia interna
- Moneda
- Precio de costo sin iva
- Precio de venta sin iva
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

