# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api
from datetime import date, timedelta


class EditPaymentTerm(models.TransientModel):
    _name = "edit.payment.term"
    _description = "Edit Payment Term"

    def edit_payment_term(self):
        pass
