# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class EditPaymentTerm(models.TransientModel):
    _name = "edit.payment.term"
    _description = "Edit Payment Term"

    element_ids = fields.Many2many(
        comodel_name='edit.payment.term.element',
        default=lambda self: self._get_default_elements()
    )

    def create_element(self, invoice_id):
        """ Crear un element desde la factura
        """
        move_obj = self.env['account.move.line']
        move_ids = move_obj.search([('invoice_id', '=', invoice_id.id)])

        element_obj = self.env['edit.payment.term.element']
        return element_obj.create(
            {'invoice_id': invoice_id.id,
             'payment_term_id': invoice_id.payment_term_id.id,
             'move_ids': [(6, False, move_ids.ids)]}
        )

    def _get_default_elements(self):
        # obtener los ids de las facturas pasadas por contexto
        ids = self._context['invoice_ids']

        # convertir los ids en un recordset
        invoice_ids = self.env['account.invoice'].browse(ids)

        # por cada factura crear un elemento y meterlo en elements
        elements = self.env['edit.payment.term.element']
        for invoice_id in invoice_ids:
            elements += self.create_element(invoice_id)
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
    payment_term_related_id = fields.Many2one(
        'account.payment.term',
        related='invoice_id.payment_term_id'
    )
    changed = fields.Boolean(
        compute="_compute_changed"
    )

    @api.depends('payment_term_id', 'payment_term_related_id')
    def _compute_changed(self):
        _ = self.payment_term_id.id != self.payment_term_related_id.id
        self.changed = _

    def write(self, vals):
        super(EditPaymentTermElement, self).write(vals)
        self.edit_maturity_date(vals['payment_term_id'])

    @api.multi
    def edit_maturity_date(self, new_payment_term_id):
        self.ensure_one()
        invoice_id = self.invoice_id

        import wdb;
        wdb.set_trace()
        # modificar el payment term de la factura
        invoice_id.payment_term_id = new_payment_term_id
