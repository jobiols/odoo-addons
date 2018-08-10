# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    item_code = fields.Char(
        help="Code from bulonfer, not shown",
        select=1
    )
    upv = fields.Integer(
        help='Agrupacion mayorista'
    )
    wholesaler_bulk = fields.Integer(
        help="Bulk Wholesaler quantity of units",
    )
    retail_bulk = fields.Integer(
        help="Bulk retail quantity of units",
    )
    invalidate_category = fields.Boolean(
        help="Category needs rebuild",
        default=False
    )
    difference = fields.Float(
        help="Difference % in cost price between invoce and bulonfer data, "
             "calculated as (invoice_price - system_price)/invoice_price"
             "this diference is an error and must go towards zero."
    )
    system_cost = fields.Float(
        compute="_compute_system_cost",
        help="Cost price based on the purchase invoice"
    )
    margin = fields.Float(
        help="Bulonfer suggested product margin from last replication"
    )
    bulonfer_cost = fields.Float(
        help="Actual cost from last actualization or from uploading a "
             "spreadsheet"
    )
    standard_price = fields.Float(
        string="Oldest Cost",
        help="The purchase cost of the oldest product in stock, after it has "
             "been delivered."
    )
    cost_history_ids = fields.One2many(
        comodel_name="stock.quant",
        inverse_name="product_tmpl_id",
        domain=[('location_id.usage', '=', 'internal')]
    )

    @api.multi
    @api.depends('bulonfer_cost', 'difference')
    def _compute_system_cost(self):
        # Calcula el costo de la factura
        for prod in self:
            prod.system_cost = prod.bulonfer_cost / (
                1 - prod.difference / 100)

    @api.multi
    def recalculate_list_price(self, margin):
        """ Recalcula los precios, verificando el precio que cargaron en la
            factura de compra. Estoy seguro de que son solo compras a bulonfer
            porque son las unicas que tienen discount_processed en True.
        """

        # TODO Revisar si esto es valido
        # buscar la linea de factura de compra que tiene el producto
        # me traigo la ultima vez que lo compre.
        invoice_lines_obj = self.env['account.invoice.line']
        for prod in self:
            invoice_line = invoice_lines_obj.search(
                [('product_id.default_code', '=', prod.default_code),
                 ('invoice_id.discount_processed', '=', True)],
                order="id desc",
                limit=1)

            p_dif = False
            if invoice_line and invoice_line.price_unit:
                # precio que cargaron en la factura de compra
                invoice_price = invoice_line.price_unit
                # descuento en la linea de factura
                invoice_price *= (1 - invoice_line.discount / 100)
                # descuento global en la factura
                invoice_price *= (1 + invoice_line.invoice_discount)
                # descuento por nota de credito al final del mes
                invoice_price *= (1 - 0.05)

                # costo que vino de bulonfer (puede ser cero)
                system_price = prod.bulonfer_cost
                if invoice_price:
                    p_dif = (invoice_price - system_price) / invoice_price

            p_dif *= 100
            prod.write({
                'list_price': prod.bulonfer_cost * (1 + margin),
                'margin': margin * 100,
                'difference': p_dif
            })

    @api.multi
    def set_cost(self, vendor_ref, cost, date, min_qty=1, vendors_code=False):
        """ Setea el costo del producto, el costo se pone en supplierinfo, no
            en standard price.

            Cuando se hace la orden de compra saca el precio y la cantidad de
            supplierinfo y luego al validarla y posteriormente ingresar la
            mercaderia el precio pasa al quant.

            Cuando se egresa mercaderia el standard_price queda al precio del
            quant que salio y segun la estrategia FIFO sale el mas antiguo.

            Poner el precio que esta en la linea mas antigua de quants en el
            standard price, si no tengo ninguno pongo el costo de hoy.

            Finalmente actualizo el bulonfer_cost que es el costo de hoy
        """
        self.ensure_one()
        for prod in self:
            vendor_id = self.env['res.partner'].search(
                [('ref', '=', vendor_ref)])
            if not vendor_id:
                raise Exception('Vendor %s not found' % vendor_ref)

            supplierinfo = {
                'name': vendor_id.id,
                'min_qty': min_qty,
                'price': cost,
                'product_code': vendors_code,  # vendors product code
                'product_name': self.name,  # vendors product name
                'date_start': date,
                'product_tmpl_id': self.id
            }

            # obtener los registros abiertos deberia haber solo uno
            sellers = self.seller_ids.search(
                [('name', '=', vendor_id.id),
                 ('product_tmpl_id', '=', self.id),
                 ('date_end', '=', False)])

            # restar un dia y cerrar los registros
            for reg in sellers:
                dt = datetime.strptime(date[0:10], "%Y-%m-%d")
                dt = datetime.strftime(dt - timedelta(1), "%Y-%m-%d")
                # asegurarse de que no cierro con fecha < start
                reg.date_end = dt if dt >= reg.date_start else reg.date_start

            # pongo un registro con el precio del proveedor
            self.seller_ids = [(0, 0, supplierinfo)]

            # buscar el quant mas antiguo de este producto, (puede no haber)
            quant_obj = self.env['stock.quant']
            quant = quant_obj.search([('product_tmpl_id', '=', prod.id)],
                                     order='in_date', limit=1)
            if quant:
                # actualizar el standard_price a este precio
                prod.standard_price = quant.cost
            else:
                # no tengo stock le pongo el costo de hoy
                prod.standard_price = cost

            # el costo hoy
            prod.bulonfer_cost = cost