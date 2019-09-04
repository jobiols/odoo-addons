# -*- coding: utf-8 -*-

# Development by:
# Salvador Daniel Pelayo <daniel@tekniu.mx>

{
    'name': 'Product Price Update Sale Order',
    'version': '1.0',
    'description': '''
    ''',
    'category': 'Other',
    'author': 'Salvador Daniel Pelayo Gómez',
    'website': 'http://tekniu.mx',
    'depends': [
        'stock', 'sale', 'sale_management', 'purchase'
    ],
    'external_dependencies': {
    },
    'data': [
        'views/price_update_view.xml',
    ],
    'application': False,
    'installable': True,
}
