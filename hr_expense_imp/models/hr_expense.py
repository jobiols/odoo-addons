# For copyright and license notices, see __manifest__.py file in module root

import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

from odoo.addons import decimal_precision as dp


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    payment_ref = fields.Integer(
        help='id de referencia al pago'
        # no ponemos el tradicional payment_id porque tomaria una referencia
        # al registro de pago y este no se podria borrar.
    )

    def return_to_approved(self):
        for rec in self:
            # verificar que no hay asientos
            if not rec.account_move_id:
                # estamos sin asientos volver a approved
                rec.write({'state': 'approve'})
                return

            # verificar que no hay apuntes contables, pero asiento vacio.
            if not rec.account_move_id.line_ids:
                # salvar el asiento (que esta vacio)
                move = rec.account_move_id
                # eliminar la relacion
                rec.account_move_id = False
                # borrar el asiento
                move.unlink()
                # estamos sin asientos volver a approved
                rec.write({'state': 'approve'})
            else:
                raise UserError(_('This expense has move lines. You cannot '
                                'return to Approved'))

    def return_to_posted(self):
        ap = self.env['account.payment']
        for rec in self:
            # verificar si hay pagos
            if not ap.search([('id', '=', rec.payment_ref)]):
                # no hay pagos, pasar a post
                rec.write(
                    {
                        'state': 'post',
                        'payment_ref': 0
                    })
            else:
                raise UserError(_('This expense has payments. You cannot '
                                'return to Posted'))
