# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    export_perception = fields.Boolean(
        compute='_compute_perception',
        default=False,
        readonly=True,
    )
    export_retention = fields.Boolean(
        compute='_compute_withholding',
        default=False,
        readonly=True,
    )

    @api.depends('tax_line_ids')
    def _compute_perception(self):
        for inv in self:
            for tax in inv.tax_line_ids.filtered(
              lambda r: r.tax_id.tax_group_id.type == 'perception'):
                inv.export_perception = True

    @api.depends('tax_line_ids')
    def _compute_withholding(self):
        for inv in self:
            for tax in inv.tax_line_ids.filtered(
              lambda r: r.tax_id.tax_group_id.type == 'withholding'):
                inv.export_withholding = True
