# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, api


class OdooBaseBackend(models.Model):
    _name = 'odoo_base.backend'
    _description = 'Odoo Base Backend'
    _inherit = 'connector.backend'

    _backend_type = 'odoo_base'

    version = fields.Selection(
            selection='_select_versions',
            string='Version',
            required=True

    )
    location = fields.Char(
            string='Location'
    )
    username = fields.Char(
            string='Username'
    )
    password = fields.Char(
            string='Password'
    )
    default_lang_id = fields.Many2one(
            comodel_name='res.lang',
            string='Default Language',
    )

    @api.model
    def _select_versions(self):
        """ Available versions
        """
        return [('9.0', 'V 9.0')]
