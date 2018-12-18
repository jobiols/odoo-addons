# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
from openerp import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    export_withholding = fields.Boolean(
        compute='_compute_withholding',
        default=False,
        readonly=True,
        store=True,
    )

    @api.multi
    @api.depends('journal_id.outbound_payment_method_ids')
    def _compute_withholding(self):
        for payment in self:
            for apm in payment.journal_id.outbound_payment_method_ids:
                if apm.code == 'withholding' and \
                        apm.payment_type == 'outbound':
                    payment.export_withholding = True
