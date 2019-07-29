# For copyright and license notices, see __manifest__.py file in module root
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import time
LINES_TO_PROCESS = 200


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.multi
    def button_confirm_bank_stepped(self, pstc):
        """ Hace lo mismo que button confirm bank pero por pasos
        """
        # hacer el balance solo en el primer step
        if pstc.step == 1:
            self._balance_check()

        statements = self.filtered(lambda r: r.state == 'open')
        for statement in statements:
            moves = self.env['account.move']
            # seleccionar las line_ids que no tengan st_line.journal_entry_ids
            # son las que no se procesaron en pasos anteriores
            lines = statement.line_ids.filtered(
                lambda r: r.journal_entry_ids.ids == [])

            # de estas lineas traer las primeras
            lines = lines[:LINES_TO_PROCESS]
            if lines:
                pstc.step += 1  # siguiente step
            else:
                pstc.write({'step': 0, 'phase': 'orders'})  # termina

            for st_line in lines:
                if st_line.account_id and not st_line.journal_entry_ids.ids:
                    st_line.fast_counterpart_creation()
                elif not st_line.journal_entry_ids.ids and \
                    not statement.currency_id.is_zero(st_line.amount):
                    raise UserError(_(
                        'All the account entries lines must be processed '
                        'in order to close the statement.'))
                for aml in st_line.journal_entry_ids:
                    moves |= aml.move_id
            if moves:
                moves.filtered(lambda m: m.state != 'posted').post()

            if pstc.step == 1:
                statement.message_post(body=_(
                    'Statement %s confirmed, journal items were created.') % (
                                                statement.name,))
        # termina, cerrar el proceso
        if pstc.step == 0:
            statements.link_bank_to_partner()
            statements.write({'state': 'confirm',
                              'date_done': time.strftime("%Y-%m-%d %H:%M:%S")})
