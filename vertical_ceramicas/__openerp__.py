# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#    Copyright (C) 2017  jeo Software  (http://www.jeosoft.com.ar)
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
# -----------------------------------------------------------------------------

{
    'name': 'Vertical Ceramicas',
    'version': '8.0.1.2',
    'category': 'Tools',
    'summary': 'Customización mayorista de ceramicas',
    'author': 'jeo Software',
    'depends': [
        'product',
        'base',
        'account',
        'stock',
        'purchase',
        # capacidad de limitar los diarios para los usuarios comerciales
        'account_multi_store',
        # capacidad de limitar los diarios para los usuarios de almacen
        'stock_multi_store',
        # Planificación 'Just in time' (bajo demanda) con inventario
        'procurement_jit_stock',
        'stock_account', 'stock_voucher'
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/account_tax_view.xml',
        'views/sale_view.xml',
        'views/pricelist_view.xml',
        'stock_report.xml',
        'views/report_stockpicking.xml',
        'views/res_company.xml',
        'views/account_invoice.xml',
        'views/res_config_view.xml',
        'views/res_product.xml',
        'views/stock_view.xml'
    ],
    'test': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
