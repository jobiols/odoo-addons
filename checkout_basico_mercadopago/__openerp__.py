# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
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
#-----------------------------------------------------------------------------------

{
    'name': 'Checkout básico mercadopago----',
    'version': '8.0.0.0',
    'category': 'Tools',
    'summary': 'gateway hacia mercadopago.',
    'author': 'jeo Software',
    'website': 'http://www.jeosoft.com.ar',
    'depends': [
        'sale'
    ],
    'data': [
        'views/account_voucher_view.xml'
#        'views/res_config_view.xml' // no lo pude hacer andar
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}

