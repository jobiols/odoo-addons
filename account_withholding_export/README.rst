.. |company| replace:: jeo Soft

.. |company_logo| image:: https://gist.github.com/jobiols/74e6d9b7c6291f00ef50dba8e68123a6/raw/fa43efd45f08a2455dd91db94c4a58fd5bd3d660/logo-jeo-150x68.jpg
   :alt: jeo Soft
   :target: https://www.jeosoft.com.ar

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

EXPORTACION DE PERCEPCIONES Y RETENCIONES
-----------------------------------------

Este modulo implementa retenciones y percepciones automaticas de ARBA y permite
exportar los archivos con los siguientes formatos:

Diseno de registro de exportacion segun documento de ARBA
https://www.arba.gov.ar/Archivos/Publicaciones/dise%C3%B1o_de_registros_bancos.pdf

1.1. Percepciones ( excepto actividad 29, 7 quincenal y 17 de Bancos)

1.7. Retenciones ( excepto actividad 26, 6 de Bancos y 17 de Bancos y No Bancos)

INSTALACION
-----------
Se requieren dependencias que estan en el repo jobiols/odoo-addons
Para que funcione hay que instalar el módulo jobiols/l10n_ar_account_withholding
y se requiere que se cargue el código CIT de Arba (es un password) que está en
la pestaña ARBA WS de mi compañía.

CONFIGURACION
-------------

**Percepciones**

Crear o actualizar el impuesto

**Nombre** Percepciones IIBB Arba aplicada
**Tipo de cálculo** codigo python
   result = price_unit * partner.get_arba_alicuota_percepcion()
**Importe Base**: Importe sin impuestos
**Etiqueta en facturas**: Perc IIBB ARBA
**Ámbito del impuesto**: Ventas
**Grupo de impuestos**: Percepción IIBB

**Retenciones**

Cuando se hace el pago lo primero es seleccionar que se va a pagar para tener
el total de deuda y luego botón calcular retenciones.

**Crear o actualizar el impuesto**

**Nombre**: Retención IIBB Arba Aplicada
**tipo**: WS Arba
**importe base**: Importe sin impuestos.

Ponerle una secuencia al impuesto con formato 0001-00000001
**Prefijo**: 0001-
**Mida de secuencia**: 8

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/jobiols/[reponame]/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------
ADHOC

Maintainer
----------

|company_logo|

This module is maintained by |company|.

To contribute to this module, please
contact Jorge Obiols <jorge.obiols@gmail.com>