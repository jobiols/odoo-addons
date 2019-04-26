# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api
from datetime import date, timedelta


class EditPaymentTermDialog(models.TransientModel):
    _name = "edit.payment.term.dialog"
    _description = "Edit Payment Term Dialog"

    date_from = fields.Date(

    )
    date_to = fields.Date(

    )

    @api.multi
    def edit_payment_term(self):
        self.ensure_one()

        # Obtener las facturas a procesar y pasarlas por contexto al wizard
        inv_obj = self.env['account.invoice']
        domain = []
        if self.date_from:
            domain.append(('date_invoice', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_invoice', '<=', self.date_to))
        invoice_ids = inv_obj.search(domain)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'edit.payment.term',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'invoice_ids': invoice_ids.ids}
        }
