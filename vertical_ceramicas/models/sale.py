# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
from openerp.exceptions import ValidationError


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # lo ponemos readonly para todos y despues lo dejamos editar con permisos
    price_unit = fields.Float(
            states={'draft': [('readonly', True)]}
    )

    @api.onchange('name')
    @api.model
    def onchange_product(self):
        """
        Ponemos un dominio al campo route_id para que traiga solo las rutas a los almacenes
        donde hay producto
        """
        for line in self:
            data = line.calc_virtual_stock(line.product_id)
            locs = []
            for loc in data:
                locs.append(loc)
                locs.append(loc + 'E')

            res = {}
            if line.product_id:
                res['domain'] = {'route_id': [('name', '=', locs)]}

        return res

    @api.model
    def product_id_change(self, ppp, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False, lang=False,
                          update_tax=True, date_order=False, packaging=False,
                          fiscal_position=False, flag=False):
        """ Hereda de la funcion product_id_change que es llamada cuando cambia el producto
            o la cantidad, se intercepta el res y se le agrega m2 en el name
        """

        res = super(sale_order_line, self).product_id_change(
                pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang,
                update_tax, date_order, packaging, fiscal_position, flag)

        if product:
            prod = self.env['product.product'].search([('id', '=', product)])
            if prod.prod_in_box != 0:
                # agregamos los metros cuadrados, al value/name. A veces el super decide
                # que no tiene que modificar el name entonces no está en el dict, en ese caso
                # lo agrego y le pongo el name_get + los metros cuadrados
                try:
                    res['value']['name'] += u' Total {} {}'.format(
                            prod.prod_in_box * qty,
                            prod.prod_in_box_uom)
                except:
                    res['value']['name'] = u'{} Total {} {}'.format(
                            prod.name_get()[0][1],
                            prod.prod_in_box * qty,
                            prod.prod_in_box_uom)
        return res

    @api.one
    @api.constrains('discount')
    def _check_discount(self):
        """ No dejar a los vendedores poner un descuento mayor que el 10%
        """
        manager = self.env['res.users'].has_group('vertical_ceramicas.group_reves_manager_users')

        if self.discount > 10 and not manager:
            raise ValidationError("No puede poner un descuento mayor que 10%")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
