# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
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
        help="Bulonfer Cost price from last replication"
    )

    oldest_cost = fields.Float(
        help="Cost price from oldest product in stock",
        compute="_compute_oldest_cost",
        digits=(7, 2)
    )

    @api.multi
    @api.depends('standard_price')
    def _compute_oldest_cost(self):
        for prod in self:
            prod.oldest_cost = prod.standard_price

    @api.multi
    @api.depends('bulonfer_cost', 'difference')
    def _compute_system_cost(self):
        # Calcula el costo de la factura basado en el costo que viene de
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

                # precio que vino de bulonfer (puede ser cero)
                system_price = prod.bulonfer_cost
                if system_price:
                    p_dif = (invoice_price - system_price) / invoice_price

            p_dif *= 100
            prod.write({
                'list_price': prod.bulonfer_cost * (1 + margin),
                'margin': margin * 100,
                'difference': p_dif
            })

    @api.multi
    def set_cost(self, vendor_id, min_qty, cost, date, vendors_code):
        """ Setea el costo del producto, el costo se pone en suplierinfo, no
            en standard price. Cuando se ingresa la mercaderia el quant queda
            valorizado al precio que esta en supplierinfo y cuando se egresa
            mercaderia el standard_price queda al precio del quant que salio.
        """

        supplierinfo = {
            'name': vendor_id.id,
            'min_qty': min_qty,
            'price': cost,
            'product_code': vendors_code,  # vendors product code
            'product_name': self.name,  # vendors product name
            'date_start': date,
            'product_tmpl_id': self.id
        }

        # si hay registros abiertos cerrarlos
        sellers = self.seller_ids.search(
            [('name', '=', vendor_id.id),
             ('product_code', '=', self.default_code),
             ('product_tmpl_id', '=', self.id),
             ('date_end', '=', False)])

        # restar un dia y cerrar las lineas si las hay
        dt = datetime.strptime(date[0:10], "%Y-%m-%d")
        dt = datetime.strftime(dt - timedelta(1), "%Y-%m-%d")
        for reg in sellers:
            reg.date_end = dt

        # crear un nuevo registro
        sellers.create(supplierinfo)
