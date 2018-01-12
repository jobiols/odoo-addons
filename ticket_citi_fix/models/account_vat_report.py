# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import base64
import logging

_logger = logging.getLogger(__name__)


class account_vat_ledger(models.Model):
    _inherit = "account.vat.ledger"

    @api.one
    def get_REGINFO_CV_CBTE(self):
        res = []
        self.invoice_ids.check_argentinian_invoice_taxes()
        if self.type == 'purchase':
            partners = self.invoice_ids.mapped('commercial_partner_id').filtered(
                lambda r: r.document_type_id.afip_code in (
                False, 99) or not r.document_number)
            if partners:
                raise Warning(_(
                    "On purchase citi, partner document is mandatory and partner document type must be different from 99. Partners %s") % partners.ids)

        for inv in self.invoice_ids:
            # only vat taxes with codes 3, 4, 5, 6, 8, 9
            # segun: http://contadoresenred.com/regimen-de-informacion-de-
            # compras-y-ventas-rg-3685-como-cargar-la-informacion/
            # empezamos a contar los codigos 1 (no gravado) y 2 (exento)
            # si no hay alicuotas, sumamos una de esta con 0, 0, 0 en detalle
            cant_alicuotas = len(inv.vat_tax_ids.filtered(
                lambda r: r.tax_code_id.afip_code in [3, 4, 5, 6, 8, 9]))
            if not cant_alicuotas and inv.vat_tax_ids.filtered(
                    lambda r: r.tax_code_id.afip_code in [1, 2]):
                cant_alicuotas = 1

            row = [
                # Campo 1: Fecha de comprobante
                fields.Date.from_string(inv.date_invoice).strftime('%Y%m%d'),

                # Campo 2: Tipo de Comprobante.
                "{:0>3d}".format(inv.afip_document_class_id.afip_code),

                # Campo 3: Punto de Venta
                self.get_point_of_sale(inv),

                # Campo 4: Número de Comprobante
                # TODO agregar estos casos de uso
                # Si se trata de un comprobante de varias hojas, se deberá informar el número de documento de la primera hoja, teniendo en cuenta lo normado en el  artículo 23, inciso a), punto 6., de la Resolución General N° 1.415, sus modificatorias y complementarias.
                # En el supuesto de registrar de manera agrupada por totales diarios, se deberá consignar el primer número de comprobante del rango a considerar.
                "{:0>20d}".format(inv.invoice_number)
            ]

            if self.type == 'sale':
                # Campo 5: Número de Comprobante Hasta.
                # TODO agregar esto En el resto de los casos se consignará el dato registrado en el campo 4
                row.append("{:0>20d}".format(inv.invoice_number))
            else:
                # Campo 5: Despacho de importación
                if inv.afip_document_class_id.afip_code == 66:
                    row.append((inv.afip_document_number or inv.number or '').rjust(
                        16, '0'))
                else:
                    row.append(''.rjust(16, ' '))

            row += [
                # Campo 6: Código de documento del comprador.
                self.get_partner_document_code(inv.commercial_partner_id),

                # Campo 7: Número de Identificación del comprador
                self.get_partner_document_number(inv.commercial_partner_id),

                # Campo 8: Apellido y Nombre del comprador.
                inv.commercial_partner_id.name.encode(
                    'ascii', 'ignore').ljust(30, ' ')[:30],

                # Campo 9: Importe Total de la Operación.
                self.format_amount(inv.amount_total, invoice=inv),

                # Campo 10: Importe total de conceptos que no integran el precio neto gravado
                self.format_amount(inv.vat_untaxed, invoice=inv),
            ]

            if self.type == 'sale':
                row += [
                    # Campo 11: Percepción a no categorizados
                    self.format_amount(
                        sum(inv.tax_line.filtered(
                            lambda
                                    r: r.tax_code_id.type == 'perception' and r.tax_code_id.tax == 'vat' and r.tax_code_id.application == 'national_taxes').mapped(
                            'tax_amount')), invoice=inv),

                    # Campo 12: Importe de operaciones exentas
                    self.format_amount(inv.vat_exempt_amount, invoice=inv),
                ]
            else:
                row += [
                    # Campo 11: Importe de operaciones exentas
                    self.format_amount(inv.vat_exempt_amount, invoice=inv),

                    # Campo 12: Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado
                    self.format_amount(
                        sum(inv.tax_line.filtered(
                            lambda
                                    r: r.tax_code_id.type == 'perception' and r.tax_code_id.tax == 'vat' and r.tax_code_id.application == 'national_taxes').mapped(
                            'tax_amount')), invoice=inv),
                ]

            row += [
                # Campo 13: Importe de percepciones o pagos a cuenta de impuestos nacionales
                self.format_amount(
                    sum(inv.tax_line.filtered(
                        lambda
                                r: r.tax_code_id.type == 'perception' and r.tax_code_id.tax != 'vat' and r.tax_code_id.application == 'national_taxes').mapped(
                        'tax_amount')), invoice=inv),

                # Campo 14: Importe de percepciones de ingresos brutos
                self.format_amount(
                    sum(inv.tax_line.filtered(
                        lambda
                                r: r.tax_code_id.type == 'perception' and r.tax_code_id.application == 'provincial_taxes').mapped(
                        'tax_amount')), invoice=inv),

                # Campo 15: Importe de percepciones de impuestos municipales
                self.format_amount(
                    sum(inv.tax_line.filtered(
                        lambda
                                r: r.tax_code_id.type == 'perception' and r.tax_code_id.application == 'municipal_taxes').mapped(
                        'tax_amount')), invoice=inv),

                # Campo 16: Importe de impuestos internos
                self.format_amount(
                    sum(inv.tax_line.filtered(
                        lambda r: r.tax_code_id.application == 'internal_taxes').mapped(
                        'tax_amount')), invoice=inv),

                # Campo 17: Código de Moneda
                str(inv.currency_id.afip_code),

                # Campo 18: Tipo de Cambio
                self.format_amount(
                    inv.currency_rate or inv.currency_id.with_context(
                        date=inv.date_invoice).compute(
                        1., inv.company_id.currency_id),
                    padding=10, decimals=6),

                # Campo 19: Cantidad de alícuotas de IVA
                str(cant_alicuotas),

                # Campo 20: Código de operación.
                # WARNING. segun la plantilla es 0 si no es ninguna
                # TODO ver que no se informe un codigo si no correpsonde,
                # tal vez da error
                inv.fiscal_position.afip_code or ' ',
            ]

            if self.type == 'sale':
                row += [
                    # Campo 21: Otros Tributos
                    self.format_amount(
                        sum(inv.tax_line.filtered(
                            lambda r: r.tax_code_id.application == 'others').mapped(
                            'tax_amount')), invoice=inv),

                    # Campo 22: vencimiento comprobante (no figura en instructivo pero si en aplicativo)
                    '00000000' if inv.point_of_sale_type == 'fiscal_controller' else
                    fields.Date.from_string(inv.date_due).strftime('%Y%m%d'),
                ]
            else:
                # Campo 21: Crédito Fiscal Computable
                if self.prorate_tax_credit:
                    if self.prorate_type == 'global':
                        row.append(self.format_amount(0), invoice=inv)
                    else:
                        # row.append(self.format_amount(0))
                        raise Warning(_('by_voucher not implemented yet'))
                else:
                    row.append(self.format_amount(inv.vat_amount, invoice=inv))

                row += [
                    # Campo 22: Otros Tributos
                    self.format_amount(
                        sum(inv.tax_line.filtered(
                            lambda r: r.tax_code_id.application == 'others').mapped(
                            'tax_amount')), invoice=inv),

                    # TODO implementar estos 3
                    # Campo 23: CUIT Emisor / Corredor
                    # Se informará sólo si en el campo "Tipo de Comprobante" se consigna '033', '058', '059', '060' ó '063'. Si para éstos comprobantes no interviene un tercero en la operación, se consignará la C.U.I.T. del informante. Para el resto de los comprobantes se completará con ceros
                    self.format_amount(0, padding=11, invoice=inv),

                    # Campo 24: Denominación Emisor / Corredor
                    ''.ljust(30, ' ')[:30],

                    # Campo 25: IVA Comisión
                    # Si el campo 23 es distinto de cero se consignará el importe del I.V.A. de la comisión
                    self.format_amount(0, invoice=inv),
                ]
            res.append(''.join(row))
        self.REGINFO_CV_CBTE = '\r\n'.join(res)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
