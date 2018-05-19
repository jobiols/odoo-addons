# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Cash Report',
    'version': '9.0.1.0',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Reporte diario para cierre de cajas',
    'author': 'jeo Software',
    'depends': [
        'account',
    ],
    'data': [
        'wizard/cashier_report_view.xml',
        'views/cashier_report.xml',
        'views/account_journal_view.xml'
    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
