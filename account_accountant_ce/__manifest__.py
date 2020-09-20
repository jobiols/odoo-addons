##############################################################################
#
#    Cubic ERP, Enterprise and Government Management Software
#    Copyright (C) 2017 Cubic ERP S.A.C. (<http://cubicerp.com>).
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
    'name': 'Accounting Management',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 35,
    'author': 'Jeo Software, Cubic ERP, Odoo',
    'license': 'AGPL-3',
    'summary': 'Financial and Analytic Accounting',
    'website': 'https://www.cubicerp.com',
    'depends': ['account_invoicing'],
    'data': [
        'data/account_accountant_data.xml',
        'security/account_accountant_security.xml',
        'views/account_accountant_templates.xml',
        'views/account_view.xml',
    ],
    'demo': ['data/account_accountant_demo.xml'],
    'test': [],
    'installable': False,
    'auto_install': False,
    'application': True,
}
