##############################################################################
#
#    Copyright (C) 2019  jeo Software  (http://www.jeosoft.com.ar)
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
##############################################################################

{
    'name': 'Product Price Update',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    "development_status": "Production/Stable",
    'summary': "Permite actualizar precios en forma masiva",
    'author': "jeo Software, Salvador Daniel Pelayo Gomez",
    'website': 'http://github.com/jobiols/odoo-addons',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'sale_management',
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/price_update_view.xml'
    ],
    'demo': [

    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
