# -*- encoding: utf-8 -*-
##################################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

{
    'name': 'Base VAT DNI - Some usefull vat / DNI validations',
    'version': '8.0.2.0',
    'category': 'Base',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Description
===========
Este modulo hace las siguientes validaciones en el numero de documento

- Si es responsable inscripto o monotributo requiere CUIT
- verifica que el DNI sea numerico
- verifica que el DNI sea unico

depende de la localizacion adhoc

    """,
    'author': 'jeo Software',
    'depends': ['l10n_ar_invoice'],
    "data": [],
    'website': 'http://jeosoft.com.ar',
    'auto_install': False,
    'installable': True,
}

