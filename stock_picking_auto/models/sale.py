# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, models, _
from openerp.exceptions import except_orm
from openerp.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_cancel(self):
        usr = self.env['res.users'].search([('id', '=', self._uid)])
        group_id = 'stock_picking_auto.group_stock_picking_auto_cashier'
        auto = usr.has_group(group_id)
        super(SaleOrder, self).action_cancel()

        if auto:
            # tiene auto, verificamos que haya 2 pickings y en done
            picking_obj = self.env['stock.picking']
            for so in self:
                state = 'done'
                pickings = so.picking_ids
                for pick in pickings:
                    if pick.state != 'done':
                        state = 'draft'

                # si hay 1 es que no lo revirtio
                if so.delivery_count < 2 or state == 'draft':
                    raise UserError("No se puede cancelar esta orden de venta "
                                    "porque ya fueron transferidos los "
                                    "productos, por favor revierta la entrega "
                                    "y reintente.\n"
                                    "Si considera que esto es un error y ya "
                                    "esta revertida haga que un usuario sin "
                                    "permiso de transferencia automatica "
                                    "cancele la orden de venta.")

    @api.multi
    def action_confirm_send(self):
        super(SaleOrder, self).action_confirm()

        picking_obj = self.env['stock.picking']
        for so in self:
            # encontrar los pickings que corresponden a la orden de venta
            for pick in picking_obj.search([('origin', '=', so.name)]):

                # forzar para que funcione aunque no haya stock
                if not pick.force_assign():
                    raise except_orm(
                        _('Can not assign product for transfer. '
                          'Unknown error'))

                if not pick.move_lines and not pick.pack_operation_ids:
                    raise UserError(_('Please create some Initial Demand or '
                                      'Mark as Todo and create some '
                                      'Operations. '))

                # In draft or with no pack operations edited yet,
                # ask if we can just do everything
                if pick.state == 'draft' or all([x.qty_done == 0.0 for x in
                                                 pick.pack_operation_ids]):
                    # If no lots when needed, raise error
                    picking_type = pick.picking_type_id
                    if (picking_type.use_create_lots or
                            picking_type.use_existing_lots):
                        for pack in pick.pack_operation_ids:
                            if pack.product_id and \
                                    pack.product_id.tracking != 'none':
                                raise UserError(_(
                                    'Some products require lots, so you need '
                                    'to specify those first!'))

                # If still in draft => confirm and assign
                if pick.state == 'draft':
                    pick.action_confirm()
                    if pick.state != 'assigned':
                        pick.action_assign()
                        if pick.state != 'assigned':
                            raise UserError(_(
                                "Could not reserve all requested products. "
                                "Please use the \'Mark as Todo\' button to "
                                "handle the reservation manually."))

                for pack in pick.pack_operation_ids:
                    if pack.product_qty > 0:
                        pack.write({'qty_done': pack.product_qty})
                    else:
                        pack.unlink()
                # TODO Revisar porque necesito un sudo aca, antes no pasaba.
                pick.sudo().do_transfer()

                return True
