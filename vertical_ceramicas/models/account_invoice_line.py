# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    # lo ponemos readonly para todos y despues lo dejamos editar con permisos
    price_unit = fields.Float(readonly=True)

    @api.one
    def _compute_price(self):
        """ Hereda de la funcion _compute_price que es llamada con un @depends cuando
            cambia la cantidad entre otras cosas el name agregando el total de metros o
            metros cuadrados de producto que hay en al caja.
        """
        super(account_invoice_line, self)._compute_price()
        if self.product_id.prod_in_box != 0:
            self.name = u'{} Total {} {}'.format(
                    self.product_id.name,
                    self.product_id.prod_in_box * self.quantity,
                    self.product_id.prod_in_box_uom)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
