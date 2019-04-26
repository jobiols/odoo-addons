# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class EditPaymentTerm(models.TransientModel):
    _name = "edit.payment.term"
    _description = "Edit Payment Term"

    element_ids = fields.Many2many(
        comodel_name='edit.payment.term.element',
    )

    def edit_payment_term(self):
        pass


class EditPaymentTermElement(models.TransientModel):
    _name = "edit.payment.term.element"
    _description = "Edit Payment Term Element"

    invoice_id = fields.Many2one(
        'account_invoice',
        required=True
    )
    date_invoice = fields.Date(
        redonly=True
    )
    date_due = fields.Date(
        redonly=True
    )
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms',
        oldname='payment_term')