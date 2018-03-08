# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields

# documentation from
# http://odoo-development.readthedocs.io/en/latest/dev/py/res.config.settings.html


class AutoloadConfigurationWizard(models.TransientModel):
    _name = 'product_autoload.settings'
    _inherit = 'res.config.settings'

    email_notification = fields.Char(
        help="Set comma separated emails for notification."
    )

    @api.model
    def get_default_email_notification(self, fields):
        us = self.env['ir.config_parameter'].get_param('email_notification', '')
        return {'email_notification': us}

    @api.multi
    def set_email_notification(self):
        value = getattr(self, 'email_notification', '')
        self.env['ir.config_parameter'].set_param('email_notification', value)
