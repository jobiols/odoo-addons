# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    export_to_sircar = fields.Boolean(
        'export_to_sircar',
        compute='_get_export_to_sircar',
        store=True
    )

    @api.one
    @api.depends('fiscal_position')
    def _get_export_to_sircar(self):
        self.export_to_sircar = 'Rio Negro' in self.fiscal_position.name if self.fiscal_position else False
