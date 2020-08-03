##############################################################################
#
#    Copyright (C) 2020  jeo Software  (http://www.jeosoft.com.ar)
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
    'name': 'Standard Dependencies CE',
    'version': '13.0.0.1.0',
    'category': 'Tools',
    'summary': "Add standard dependecies for Argentinian localization",
               "on Community Edition",
    'author': "jeo Software",
    'website': 'http://github.com/jobiols/module-repo',
    'license': 'AGPL-3',
    'depends': [
        # para la localizacion argentina version Enterprise
        'l10n_ar_edi', # Factura electronica Argentina
        'l10n_ar_ux', # Mejoras para argentina, cheques y medios de pago
        'l10n_ar_bank',  # Bancos Argentinos
#        'l10n_ar_reports', # Libros de IVA Digital (ENTERPRISE)
        'l10n_ar_stock', # Remitos COT y req Argentinos

        #'l10n_ar_account_withholding' # Este tiene problemas

        # Para mejorar la usabilidad
        'base_currency_inverse_rate',  # TC en Argentino
        'account_ux',  # hace pilas de cosas ver en el modulo
        'base_ux',  # mejoras de base
        'product_ux',  # mejoras en productos
        'sale_ux',  # mejoras en ventas
        'auto_backup',  # poner el backup en: /var/odoo/backups/
        'mail_activity_board_ux',  # quitar actividades del chatter
        #'partner_ref_unique',  # evita duplicados en referencia
        #'partner_vat_unique',  # evita duplicados numeros de referencia
        #'product_unique',  # no se pueden duplicar codigos de producto
        #'web_export_view',  # exportar cualquier vista en excel
        # 'account_clean_cancelled_invoice_number',  # no esta migrado
    ],
    'data': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
