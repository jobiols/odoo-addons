# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields


PARAMS = [
    ("email_notification", 'email_notification'),
    ("last_replication", 'last_replication'),
    ("import_only_new", 'import_only_new'),
    ("data_path", 'data_path'),
    ("email_from", 'email_from')
]


class AutoloadConfigurationWizard(models.TransientModel):
    _name = 'product_autoload.settings'
    _inherit = 'res.config.settings'

    email_notification = fields.Char(
        help="Set comma separated emails for notification."
    )

    last_replication = fields.Datetime(
        help="Date and time of last replication"
    )

    import_only_new = fields.Boolean(
        help="Import only new registers",
    )

    data_path = fields.Char(
        help="path to data files on server",
    )
    email_from = fields.Char(
        help="Email Sender i.e. 'Bulonfer SA <noresponder@bulonfer.com.ar>'"
    )

    @api.multi
    def set_params(self):
        self.ensure_one()
        for field_name, key_name in PARAMS:
            value = getattr(self, field_name, '')
            self.env['ir.config_parameter'].set_param(key_name, value)

    @api.multi
    def get_default_params(self, fields):
        res = dict()
        for field_name, key_name in PARAMS:
            value = self.env['ir.config_parameter'].get_param(key_name, False)
            res[field_name] = value
        return res
