# For copyright and license notices, see __manifest__.py file in module root

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        """ Cuando se selecciona un producto en la linea de factura (venta)
            se revisa si tiene customer_ids, y si es asi se busca para el
            cliente de esa venta cual es el nombre correcto y se lo pone en
            el name de la linea.
        """
        ret = super(SaleOrderLine, self).product_id_change()

        if self.product_id.customer_ids:
            si_obj = self.env['product.customerinfo']
            today = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            cust_info = si_obj.search([
                ('name', '=', self.order_id.partner_id.id),
                ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id),
                '|', ('date_start', '<=', today), ('date_start', '=', False),
                '|', ('date_end', '>=', today), ('date_end', '=', False)])

            if cust_info:
                self.name = '[{}] {}'.format(cust_info.product_code,
                                             cust_info.product_name)

        return ret
