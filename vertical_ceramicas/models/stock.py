# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # es el comentario del deposito se usa en el remito para decir donde se
    # retira y a que hora etc.
    pick_from = fields.Char(
        string="retira",
        compute="_get_picking_location"
    )
    printed = fields.Boolean(
        string="Imp",
        help="Indica si el remito fue impreso por un encargado de deposito"
    )
    carrier = fields.Char(
        'Transportista'
    )

    min_only_date = fields.Date(
        compute='_get_min_only_date',
        store=True
    )

    @api.one
    @api.depends('min_date')
    def _get_min_only_date(self):
        """ creamos una nueva min_date porque necesito truncar la parte de
            hora y asi filtrar por dias.
        """
        self.min_only_date = self.min_date

    @api.one
    def _get_picking_location(self):
        for line in self.move_lines:
            loc = line.location_id
            self.pick_from = loc.comment

    @api.multi
    def mark_as_printed(self):
        for reg in self:
            user = self.env['res.users'].search([('id', '=', self._uid)])
            group = self.env['res.groups'].search([('name', '=', u'Almacén')])

            # marco como impreso solo si lo imprime un usuario de deposito.
            if user in group.users:
                reg.printed = True


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
        addresses = self.partner_id.child_ids.search(
            [('type', '=', 'delivery')])
        # me traigo solo la primera si es que existe
        for address in addresses:
            self.partner_shipping_id = address.id

# intento de poner los stores en el nombre de las rutas
# class StockLocationRoute(models.Model):
#    _inherit = 'stock.location.route'
#    _rec_name = 'id'

#    @api.multi
#    def name_get(self):
#        for rec in self:
#            return [str(rec.id)+'pp']
