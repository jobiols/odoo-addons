# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    'name': 'Exportacion de percepciones y retenciones',
    'version': '9.0.0.0.0',
    'website': 'http://jeosoft.com.ar',
    'author': 'jeo Software',
    'category': 'Accounting',
    'depends': [
        'l10n_ar_account_vat_ledger',
        'l10n_ar_account_withholding',
    ],
    "data": [
        'views/account_report_view.xml',
        'views/account_tax_view.xml',
    ],
    'auto_install': False,
    'installable': True,
}
