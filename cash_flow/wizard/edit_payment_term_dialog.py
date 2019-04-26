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
        action = self.env.ref('cash_flow.action_edit_payment_term')
        return {
            'type': action.type,
            'res_model': action.res_model,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
        }
