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
    'name': 'Account Journal Report by Date',
    'version': '8.0.1.0.0',
    'category': 'Support',
    'sequence': 15,
    'summary': '',
    'description': """
Account Journal Report by Date
==============================
account.account_common_report_view
En el reporte de diarios agrega la posibilidad de filtrar por fecha
Contabilidad / Reportes legales / Diarios / Diarios

    """,
    'author':  'jeo Soft',
    'website': 'jeosoft.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'account'
    ],
    'data': [
        'views/account_financial_report_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
