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
    'name': 'Shadow User',
    'version': '13.0.0.0.0',
    'category': 'Tools',
    'summary': "Agrega permisos especiales al usuario",
    'author': "jeo Software",
    'website': 'http://github.com/jobiols/odoo-addons',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_debt_management',
        'l10n_ar_chart',
        'l10n_ar_account',

        # se requieren para que corran los test
        'sale_management'
    ],
    'data': [
        'security/res_groups.xml',
        'views/account_journal_form.xml'
    ],
    'demo': [
        'data/data.xml',
        'data/configuration.yml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
    'customer': 'Virtual Dreams',
}
