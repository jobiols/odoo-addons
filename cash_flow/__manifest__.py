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
    'name': 'Cash Flow',
    'version': '13.0.0.0.0',
    'category': 'Accounting',
    'summary': "Cash Flow Management",
    'author': "NTSystemWork",
    'development_status': 'Production',
    'website': 'http://github.com/ntsystemwork',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'l10n_ar_chart',
        'sale_management'
    ],
    'data': [
        'wizard/cash_flow_view.xml',
        'wizard/edit_payment_term_dialog_view.xml',
        'wizard/edit_payment_term_view.xml',
        'reports/cash_flow_report.xml',
        'views/forecast_view.xml',
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml'
    ],
    'demo': [
        'data/configuration.yml',
        'data/journals.xml',
    ],
    'installable': False,
    'application': False,
}
