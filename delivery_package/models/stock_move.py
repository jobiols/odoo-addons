# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    packages = fields.Integer(
        compute="_compute_packages"
    )

    def _compute_packages(self):
        for rec in self:
            pack = 0
            for line in rec.move_lines:
                pack += line.packages
            rec.packages = pack


class StockMove(models.Model):
    _inherit = "stock.move"

    packages = fields.Integer(
        'Bulto',
        help='Cantidad de elementos en el bulto'
    )


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    packages = fields.Integer(
        related="move_id.packages",
        help='Cantidad de elementos en el bulto',
        readonly=True
    )
