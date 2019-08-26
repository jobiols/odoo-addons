# For copyright and license notices, see __manifest__.py file in module root


from odoo import api, exceptions, fields, models, _

DISCOUNTS = [
             ('3.0', '3 %'),
             ('5.0', '5 %'),
             ('10.0', '10 %')]


class ResPartner(models.Model):
    _inherit = "res.partner"

    discount1 = fields.Selection(
        DISCOUNTS,
        string='Desc A',
    )
    discount2 = fields.Selection(
        DISCOUNTS,
        string='Desc B',
    )
    discount3 = fields.Selection(
        DISCOUNTS,
        string='Desc C',
    )
