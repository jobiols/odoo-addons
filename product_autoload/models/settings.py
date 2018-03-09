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

    last_replication = fields.Datetime(
        help="Date and time of last replication"
    )

    import_only_new = fields.Boolean(
        help="Import only new registers",
    )

    data_path = fields.Char(
        help="path to data files on server",
    )

    @api.model
    def get_default_email_notification(self, fields):
        value = self.env['ir.config_parameter'].get_param(
            'email_notification', '')
        return {'email_notification': value}

    @api.multi
    def set_email_notification(self):
        value = getattr(self, 'email_notification', '')
        self.env['ir.config_parameter'].set_param('email_notification', value)

    @api.model
    def get_default_last_replication(self, fields):
        value = self.env['ir.config_parameter'].get_param(
            'last_replication', '')
        return {'last_replication': value}

    @api.multi
    def set_last_replication(self):
        value = getattr(self, 'last_replication', '')
        self.env['ir.config_parameter'].set_param('last_replication', value)

    @api.model
    def get_default_import_only_new(self, fields):
        value = self.env['ir.config_parameter'].get_param(
            'import_only_new', True)
        return {'import_only_new': value}

    @api.multi
    def set_import_only_new(self):
        value = getattr(self, 'import_only_new', True)
        self.env['ir.config_parameter'].set_param('import_only_new', value)

    @api.model
    def get_default_data_path(self, fields):
        value = self.env['ir.config_parameter'].get_param(
            'data_path', '/opt/odoo/data/product_data/')
        return {'data_path': value}

    @api.multi
    def set_data_path(self):
        value = getattr(self, 'data_path', '')
        self.env['ir.config_parameter'].set_param('data_path', value)

