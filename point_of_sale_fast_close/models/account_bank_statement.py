# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import float_is_zero, pycompat
from odoo.tools import float_compare, float_round, float_repr
from odoo.tools.misc import formatLang, format_date
from odoo.exceptions import UserError, ValidationError

import time
import math


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.multi
    def button_confirm_bank_stepped(self, stc):
        """ Hace lo mismo que button confirm bank pero por pasos
        """
        # hacer el balance solo en el primer step
        if stc.step == 1:
            self._balance_check()

        statements = self.filtered(lambda r: r.state == 'open')
        for statement in statements:
            moves = self.env['account.move']

            # traer solo 100 lineas
            lines = statement.line_ids.search([], limit=2)
            if lines:
                stc.step += 1  # siguiente step
            else:
                stc.write({'step': 0, 'phase': 'orders'})  # termina

            for st_line in lines:
                if st_line.account_id and not st_line.journal_entry_ids.ids:
                    st_line.fast_counterpart_creation()
                elif not st_line.journal_entry_ids.ids and not statement.currency_id.is_zero(st_line.amount):
                    raise UserError(_(
                        'All the account entries lines must be processed in order to close the statement.'))
                for aml in st_line.journal_entry_ids:
                    moves |= aml.move_id
            if moves:
                moves.filtered(lambda m: m.state != 'posted').post()

            if stc.step == 1:
                statement.message_post(body=_(
                    'Statement %s confirmed, journal items were created.') % (
                                            statement.name,))

        # termina cerrar el proceso
        if stc.step == 0:
            statements.link_bank_to_partner()
            statements.write({'state': 'confirm',
                              'date_done': time.strftime("%Y-%m-%d %H:%M:%S")})
