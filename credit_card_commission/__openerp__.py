# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2017 jeo Software#    (www.jeosoft.com.ar).#
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
##############################################################################

{
    'name': 'Credit Card Commission Calculator',
    'version': '8.0.1.0.0',
    'author': 'jeo Software',
    'maintainer': 'Jorge Obiols <jorge.obiols@gmail.com>',
    'website': 'www.jeosoft.com.ar',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml # noqa
    # for the full list
    'category': 'Tools', 'summary': 'Computes credit card commissions',

    # any module necessary for this one to work correctly
    'depends': [
        'product',
    ],
    'external_dependencies': {
        'python': [],
    },

    # always loaded
    'data': [
        'views/card_view.xml',
        'views/card_commission_view.xml',
        'views/product_view.xml',
        'data/card_data.xml',
        'views/credit_plan_view.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    # used for Javascript Web CLient Testing with QUnit / PhantomJS
    # https://www.odoo.com/documentation/8.0/reference/javascript.html#testing-in-odoo-web-client  # noqa
    'js': [],
    'css': [],
    'qweb': [],

    'installable': True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    'auto_install': False,
    'application': False,
}
