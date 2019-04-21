##############################################################################
#
#    Copyright (C) 2015  JEOSOFT  (http://www.jeosoft.com.ar)
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
    'name': 'Support branding JEOSOFT',
    'version': '11.0.0.0.0',
    'category': 'Support',
    'sequence': 14,
    'summary': '',
    'author':  'jeo Soft',
    'website': 'jeosoft.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        # requeridos por este modulo
        'support_branding',
        'mail',

        # para la localizacion argentina
        'l10n_ar_base',  # esto se instala solo
        'l10n_ar_account',  # esto se instala solo
        'l10n_ar_afipws_fe',        # Factura Electrónica Argentina
        'l10n_ar_aeroo_einvoice',   # impresion de factura electronica aeroo
        'l10n_ar_account_vat_ledger_citi',
        'account_debt_management',  #
        'l10n_ar_aeroo_payment_group',  #

        # modulos adicionales utilitarios
        'disable_odoo_online',  # Elimina menu de odoo online
        'res_config_settings_enterprise_remove',  # Elimina menus enterprise
        'auto_backup',  # poner el backup en: /var/odoo/backups/
        'backend_theme',
        'server_mode',          # server_mode = "test" en desarrollo
        'due_payments_argentina_fix'  # corrige nombres de documentos
    ],
    'data': [
        'views/ir_config_parameter.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
