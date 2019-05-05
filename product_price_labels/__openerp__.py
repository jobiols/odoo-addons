# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Price Labels',
    'version': '8.0.0.0.0',
    'category': 'Tools',
    'summary': 'Impresion de etiquetas de productos',
    'author': 'jeo Software',
    'depends': [
        'product'
    ],
    'data': [
       'reports/price_labels_report.xml'
    ],
    'test': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
