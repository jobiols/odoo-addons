# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    export_perception = fields.Boolean(
        compute='_compute_perception',
        default=False,
        readonly=True,
        store=True,
        help='Marca si la factura tiene percepciones'
    )

    @api.multi
    @api.depends('tax_line_ids')
    def _compute_perception(self):
        for inv in self:
            for tax in inv.tax_line_ids.filtered(
                lambda r: r.tax_id.tax_group_id.type == 'perception'):  # noqa
                inv.export_perception = True
