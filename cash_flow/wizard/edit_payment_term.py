# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class EditPaymentTerm(models.TransientModel):
    _name = "edit.payment.term"
    _description = "Edit Payment Term"

    element_ids = fields.Many2many(
        comodel_name='edit.payment.term.element',
        default=lambda self: self._get_default_elements()
    )

    def _get_default_elements(self):
        # obtener los ids de las facturas pasadas por contexto
        ids = self._context['invoice_ids']
        # convertir los ids en un recordset
        invoice_ids = self.env['account.invoice'].browse(ids)
        # obtener el objeto elements y una variable donde sumar
        elements = element_obj = self.env['edit.payment.term.element']
        # por cada factura crear un elemento y meterlo en elements
        for invoice_id in invoice_ids:
            elements += element_obj.create(
                {'invoice_id': invoice_id.id,
                 'payment_term_id': invoice_id.payment_term_id.id})
        return elements

    def edit_payment_term(self):
        pass


class EditPaymentTermElement(models.TransientModel):
    _name = "edit.payment.term.element"
    _description = "Edit Payment Term Element"

    invoice_id = fields.Many2one(
        'account.invoice',
        required=True,
        readonly=True
    )
    date_invoice = fields.Date(
        related='invoice_id.date_invoice',
        redonly=True
    )
    date_due = fields.Date(
        related='invoice_id.date_due',
        redonly=True
    )
    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        oldname='payment_term'
    )
