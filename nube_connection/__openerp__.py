# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tienda Nube Connection',
    'version': '8.0.1.4',
    'category': 'Tools',
    'summary': 'Conexion con tienda nube',
    'author': 'jeo Software',
    'depends': [
        'curso',
        'product'
    ],
    'data': [
        'views/product_view.xml',
        'views/woo_categ_view.xml',
        'security/ir.model.access.csv'
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
