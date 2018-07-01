# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    invoice_discount = fields.Float(
        string='Invoice Discount',
        default=False,
        help="the discount that applied to the purchase price minus the "
             "discount line gives the actual purcahse price. If there is no"
             "global discount then it is 0%"
    )


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    discount_processed = fields.Boolean(
        default=False,
        help='Shows wether this invoice was processed with invoice_discounts'
    )

    @api.one
    def compute_invoice_discount(self):
        prod_iva_21 = disc_iva_21 = prod_iva_105 = disc_iva_105 = 0
        for line in self.invoice_line_ids:
            # el subtotal de la linea
            subtotal = line.price_unit * (
                1 - line.discount / 100) * line.quantity

            # sumar IVA 21%
            if line.invoice_line_tax_ids[0].amount == 21.0:
                if line.product_id:
                    # sumar subtotales con el descuento de linea aplicado
                    prod_iva_21 += subtotal
                else:
                    # sumar descuentos (no tienen producto)
                    disc_iva_21 += subtotal

            # sumar IVA 10.5%
            if line.invoice_line_tax_ids[0].amount == 10.5:
                if line.product_id:
                    # sumar subtotales con el descuento de linea aplicado
                    prod_iva_105 += subtotal
                else:
                    # sumar descuentos (no tienen producto)
                    disc_iva_105 += subtotal

        disc_21 = disc_iva_21 / prod_iva_21 if prod_iva_21 else False
        disc_105 = disc_iva_105 / prod_iva_105 if prod_iva_105 else False

        # ponerle el descuento global a todas las lineas
        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids[0].amount == 21.0 and line.product_id:
                line.invoice_discount = disc_21

            if line.invoice_line_tax_ids[0].amount == 10.5 and line.product_id:
                line.invoice_discount = disc_105

        self.discount_processed = True
