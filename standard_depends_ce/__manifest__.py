##############################################################################
#
#    Copyright (C) 2019  jeo Software  (http://www.jeosoft.com.ar)
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
    'version': '12.0.0.1.0',
    'category': 'Tools',
    'summary': "Add standard dependecies for Argentinian localization",
    'author': "jeo Software",
    'website': 'http://github.com/jobiols/module-repo',
    'license': 'AGPL-3',
    'depends': [
        # para la localizacion argentina version comunitaria
        'l10n_ar_base',  # esto se instala solo
        'l10n_ar_account',  # esto se instala solo
        'l10n_ar_afipws_fe',  # Factura Electrónica Argentina
        'l10n_ar_aeroo_einvoice',  # impresion de factura electronica aeroo
        'l10n_ar_account_vat_ledger_citi',  # Reportes citi
        'account_debt_management',  # mejoras en administracion de deudas
        'l10n_ar_aeroo_payment_group',  # Pagos
        'l10n_ar_account_withholding',  # Retenciones
        'account_accountant',           # permisos para contabilidad

        # modulos adicionales utilitarios CE
        'base_ux',  # mejoras de base
        'account_ux',  # hace pilas de cosas ver en el modulo
        'sale_ux',  # mejoras en ventas
        'disable_odoo_online',  # Elimina menu de odoo online
        #'res_config_settings_enterprise_remove',  # Elimina menus enterprise
        'auto_backup',  # poner el backup en: /var/odoo/backups/
        #'backend_theme',
        'server_mode',          # server_mode = "test" en desarrollo
        'partner_ref_unique',  # evita duplicados en referencia
        'partner_vat_unique',  # evita duplicados numeros de referencia
        #'mail_activity_board_ux',  # quitar actividades del chatter
        'product_unique',  # no se pueden duplicar codigos de producto

        # fixes
        #'invoice_lines_analysis_fix',  # corrige bug en pivot
    ],
    'data': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
