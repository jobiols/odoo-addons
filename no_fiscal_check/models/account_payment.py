# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    fiscal = fields.Selection([
        ('fiscal', 'Fiscal'),
        ('no_fiscal', 'No Fiscal')],
        help='Marca de cheque no fiscal',
        default='fiscal'
    )

    def create_check(self, check_type, operation, bank):
        check = super(AccountPayment, self).create_check(check_type,
                                                         operation, bank)
        check.fiscal = self.fiscal
        return check


class AccountCheck(models.Model):
    _inherit = 'account.check'

    fiscal = fields.Selection([
        ('fiscal', 'Fiscal'),
        ('no_fiscal', 'No Fiscal')],
        help='Marca de cheque no fiscal',
        default='fiscal'
    )
