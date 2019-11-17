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
from openerp import fields, models, api

#http://odoo-development.readthedocs.io/en/latest/dev/py/res.config.settings.html
class AccountPaymentConfig(models.TransientModel):
    _inherit = 'account.config.settings'
#    _name = 'mercadopago.settings'

    # como empieza con _module el execute iniciará la instalación del modulo checkout_basico_mercadopago
    module_checkout_basico_mercadopago = fields.Boolean(
            'Manage Payments Using Mercadopago',
            help='-It installs the module checkout_basico_mercadopago.'
        )
    mercadopago_client_id = fields.Char('client id')
    mercadopago_client_secret = fields.Char('cliente secret')

    @api.one
    def set_mercadopago_client_id(self):
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param('mercadopago_client_id', self.mercadopago_client_id or '')

    @api.one
    def set_mercadopago_client_secret(self):
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param('mercadopago_client_secret', self.mercadopago_client_secret or '')

    @api.model
    def get_mercadopago_client_id(self, fields):
        client_id = self.env['ir.config_parameter'].get_param('mercadopago_client_id', default=False)
        self.mercadopago_client_id = client_id

    @api.model
    def get_mercadopago_client_secret(self, fields):
        client_secret = self.env['ir.config_parameter'].get_param('mercadopago_client_secret', default=False)
        self.mercadopago_client_secret = client_secret


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
