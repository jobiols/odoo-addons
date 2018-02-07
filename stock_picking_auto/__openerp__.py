# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock picking automatic',
    'version': '9.0.0.0',
    'category': 'Warehouse Management',
    'author': "jeo Software",
    'website': 'http://www.jeosoft.com.ar',
    'depends': [
        'base',
        'sale',
        'stock'
    ],
    'data': [
        'security/security_groups.xml',
        'views/sale_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': "AGPL-3",
}
