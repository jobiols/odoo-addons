# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields


class EditPaymentTerm(models.TransientModel):
    _name = "edit.payment.term"
    _description = """
    Este objeto aloja los edit.payment.term.element, Cada uno de estos
    contiene los datos necesarios para modificar las fechas de vencimiento de
    una factura.
    Las facturas a editar se seleccionan en el edit.payment.term.dialog
    """

    element_ids = fields.Many2many(
        comodel_name='edit.payment.term.element',
        default=lambda self: self._get_default_elements()
    )

    def create_element(self, invoice_id):
        """ Crear un element desde la factura
        """
        aml_obj = self.env['account.move.line']
        # Obtenemos las lineas de asiento de la factura que tienen la
        # cuenta Deudores por ventas (2) o proveedores (1)
        amls = aml_obj.search([('invoice_id', '=', invoice_id.id),
                               '|', ('account_id', '=', 2),
                               ('account_id', '=', 55)])

        element_obj = self.env['edit.payment.term.element']
        return element_obj.create(
            {'invoice_id': invoice_id.id,
             'line_ids': [(6, 0, amls.ids)]}
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
    _description = """
    Este objeto tiene todos los datos necesarios para editar las fechas de
    vencimiento de una factura
    """

    invoice_id = fields.Many2one(
        'account.invoice',
        required=True,
        readonly=True
    )
    display_name = fields.Char(
        related='invoice_id.display_name',
        readonly=True
    )
    date_invoice = fields.Date(
        related='invoice_id.date_invoice',
        redonly=True
    )
    residual = fields.Monetary(
        related='invoice_id.residual',
        readonly=True
    )
    date_due = fields.Date(
        related='invoice_id.date_due',
        readonly=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='invoice_id.currency_id',
        readonly=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        related='invoice_id.partner_id',
        readonly=True
    )
    payment_term_id = fields.Many2one(
        'account.payment.term',
        related='invoice_id.payment_term_id',
        readonly=True
    )
    line_ids = fields.Many2many(
        'account.move.line',
    )

    def write(self, values):
        super(EditPaymentTermElement, self).write(values)

        # obtener la fecha del ultimo pago para ponerla en la factura
        # hay que buscar en las move lines porque la fecha modificada puede
        # no ser la ultima. Y en la factura va la fecha del ultimo pago
        aml_obj = self.env['account.move.line']
        amls = aml_obj.search([('invoice_id', '=', self.invoice_id.id),
                               '|', ('account_id', '=', 2),
                               ('account_id', '=', 55)],
                              limit=1,
                              order='date_maturity desc')

        # cambiar la fecha de vencimiento de la factura.
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.search([('id', '=', self.invoice_id.id)])
        invoice.date_due = amls.date_maturity
