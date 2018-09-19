# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Cash Report',
    'version': '11.0.0.0.0',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Reporte diario para cierre de cajas',
    'author': 'jeo Software',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/cash_view.xml',
        'wizard/cashier_report_view.xml',
        'views/cashier_report.xml',
        'views/account_journal_view.xml',
        'views/res_users_view.xml',
        'views/invoice_report.xml'
    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': False,
    'application': False,
    'auto_install': False,
    'images': [],
}
