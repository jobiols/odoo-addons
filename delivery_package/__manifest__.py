# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Bultos en Remitos",
    "summary": "Agrega bultos en las lineas de remito",
    "version": "13.0.0.0.0",
    "development_status": "Alpha",
    "category": "Inventory",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    'customer': 'Virtual Dreams',
    "depends": [
        'stock',
        'l10n_ar_aeroo_stock',
    ],
    "data": [
        'report/invoice_report.xml',
        'views/stock_move_view.xml'
    ],
    'installable': False,

}
