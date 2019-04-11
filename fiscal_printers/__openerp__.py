# -*- coding: utf-8 -*-
{
    'name': "Fiscal Printers",
    'summary': """Manejo de impresoras FISCALES""",
    'author': "Avalon, Martin Anchordoqui, jeo Software Jorge Obiols",
    'website': "http://www.avalonsis.com",
    'category': 'Accounting',
    'version': '9.0.0.5.0',
    'depends': [
        'account',
        'point_of_sale'
    ],
    'data': [
        'views/partner_view.xml',
        'views/journal_view.xml',
        'views/POS_view.xml',
        'views/view_pos_session.xml',
    ],
    'qweb': ['point_of_sale'],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': [
            'pyfiscalprinter'
        ]
    }
}
