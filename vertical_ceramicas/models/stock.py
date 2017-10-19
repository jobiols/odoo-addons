# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # es el comentario del deposito se usa en el remito para decir donde se retira y a que hora etc.
    pick_from = fields.Char(
            string="retira",
            compute="_get_picking_location"
    )

    @api.one
    def _get_picking_location(self):
        for line in self.move_lines:
            loc = line.location_id
            self.pick_from = loc.comment


class StockMove(models.Model):
    _inherit = "stock.move"

    # es la direccion de entrega
    partner_shipping_id = fields.Many2one(
            'res.partner',
            'Direccion de entrega',
            compute='_get_partner_shipping_id'
    )

    @api.one
    @api.depends('partner_id.child_ids')
    def _get_partner_shipping_id(self):
        addresses = self.partner_id.child_ids.search([('type', '=', 'delivery')])
        # me traigo solo la primera si es que existe
        for address in addresses:
            self.partner_shipping_id = address.id



