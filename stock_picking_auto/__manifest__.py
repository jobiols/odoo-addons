# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock picking automatic',
    'version': '11.0.0.0.0',
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
    'installable': False,
    'auto_install': False,
    'application': False,
    'license': "AGPL-3",
}
