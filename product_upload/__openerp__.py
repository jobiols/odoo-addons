# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
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
# -----------------------------------------------------------------------------
{
    'name': 'Product Upload',
    'version': '9.0.0.0.0',
    'license': 'AGPL-3',
    'category': 'Tools',
    'summary': 'Crear / Actualizar productos',
    'author': 'jeo Software',
    'depends': [
        'stock',
        'product_autoload',
        'product_currency',
        'simple_meli_publishing'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_worksheet_view.xml',
        'security/security_groups.xml',
        'views/log_view.xml',
        'views/error_view.xml',
    ],
    'test': [
    ],
    'demo': [
        'data/partner_data.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
    'external_dependencies': {
        'python': [
            'openpyxl',
        ],
    },
}
