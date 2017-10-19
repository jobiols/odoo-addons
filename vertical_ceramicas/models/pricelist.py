# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class product_pricelist(models.Model):
    _inherit = "product.pricelist"

    # Para que los vendedores no accedan a ciertas listas de precio.
    restricted = fields.Boolean(
        'Restringido'
    )


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
