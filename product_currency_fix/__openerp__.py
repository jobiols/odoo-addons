# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
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
##############################################################################
{
    'name': 'Product Currency fix',
    'version': '9.0.0.0.0',
    'category': 'Contabilidad',
    'author': 'jeo Software',
    'website': 'http://jeosoft.com.ar/',
    'license': 'AGPL-3',
    'depends': [
        'product_currency',
        'stock',
        'stock_account',
        'purchase',
        'product_autoload' # quitar esta dependencia
    ],
    'data': [
        'views/product_template_view.xml'
    ],
    'installable': True,
}
