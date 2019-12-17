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
    'name': 'Quotation report improved',
    'version': '13.0.0.0.0',
    'category': 'Tools',
    'summary': "Adds customer data to quotation report",
    'author': "jeo Software",
    'license': 'AGPL-3',
    'depends': [
        'sale'
    ],
    'data': [
        'views/sale_order_form.xml',
        'report/quotation_report_template.xml'
    ],
    'demo': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
    'customer': 'Virtual Dreams',
    'maturity': 'Stable'
}
