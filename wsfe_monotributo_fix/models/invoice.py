# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2017  jeo Software  (http://www.jeosoft.com.ar)
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
from openerp import fields, models, api, _
from openerp.exceptions import Warning
from cStringIO import StringIO as StringIO
import logging
import sys
import traceback
_logger = logging.getLogger(__name__)

try:
    from pysimplesoap.client import SoapFault
except ImportError:
    _logger.debug('Can not `from pyafipws.soap import SoapFault`.')


class invoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def do_pyafipws_request_cae(self):
        "Request to AFIP the invoices' Authorization Electronic Code (CAE)"
        for inv in self:
            # Ignore invoices with cae
            if inv.afip_auth_code and inv.afip_auth_code_due:
                continue

            afip_ws = inv.journal_id.point_of_sale_id.afip_ws
            # Ignore invoice if not ws on point of sale
            if not afip_ws:
                continue

            # get the electronic invoice type, point of sale and afip_ws:
            commercial_partner = inv.commercial_partner_id
            country = commercial_partner.country_id
            journal = inv.journal_id
            point_of_sale = journal.point_of_sale_id
            pos_number = point_of_sale.number
            doc_afip_code = inv.afip_document_class_id.afip_code

            # authenticate against AFIP:
            ws = inv.company_id.get_connection(afip_ws).connect()

            next_invoice_number = inv.next_invoice_number

            # get the last invoice number registered in AFIP
            if afip_ws == "wsfe" or afip_ws == "wsmtxca":
                ws_invoice_number = ws.CompUltimoAutorizado(
                    doc_afip_code, pos_number)
            elif afip_ws == 'wsfex':
                ws_invoice_number = ws.GetLastCMP(
                    doc_afip_code, pos_number)
                if not country:
                    raise Warning(_(
                        'For WS "%s" country is required on partner' % (
                            afip_ws)))
                elif not country.code:
                    raise Warning(_(
                        'For WS "%s" country code is mandatory'
                        'Country: %s' % (
                            afip_ws, country.name)))
                elif not country.afip_code:
                    raise Warning(_(
                        'For WS "%s" country afip code is mandatory'
                        'Country: %s' % (
                            afip_ws, country.name)))

            ws_next_invoice_number = int(ws_invoice_number) + 1
            # verify that the invoice is the next one to be registered in AFIP
            if next_invoice_number != ws_next_invoice_number:
                raise Warning(_(
                    'Error!'
                    'Invoice id: %i'
                    'Next invoice number should be %i and not %i' % (
                        inv.id,
                        ws_next_invoice_number,
                        next_invoice_number)))

            partner_doc_code = commercial_partner.document_type_id.afip_code
            tipo_doc = partner_doc_code or '99'
            nro_doc = (
                partner_doc_code and commercial_partner.document_number or "0")
            cbt_desde = cbt_hasta = cbte_nro = next_invoice_number
            concepto = tipo_expo = int(inv.afip_concept)

            fecha_cbte = inv.date_invoice
            if afip_ws != 'wsmtxca':
                fecha_cbte = fecha_cbte.replace("-", "")

            # due and billing dates only for concept "services"
            if int(concepto) != 1:
                fecha_venc_pago = inv.date_due
                fecha_serv_desde = inv.afip_service_start
                fecha_serv_hasta = inv.afip_service_end
                if afip_ws != 'wsmtxca':
                    fecha_venc_pago = fecha_venc_pago.replace("-", "")
                    fecha_serv_desde = fecha_serv_desde.replace("-", "")
                    fecha_serv_hasta = fecha_serv_hasta.replace("-", "")
            else:
                fecha_venc_pago = fecha_serv_desde = fecha_serv_hasta = None

            # # invoice amount totals:
            imp_total = str("%.2f" % abs(inv.amount_total))

            ## wsfe_monotributo_fix

            # ImpTotConc es el iva no gravado, si es Comprobante C debe ser 0.00
            if doc_afip_code != 11 and doc_afip_code != 13:
                imp_tot_conc = str("%.2f" % abs(inv.vat_untaxed))
            else:
                imp_tot_conc = "0.00"

            if doc_afip_code != 11 and doc_afip_code != 13:
                # en la v9 lo hicimos diferente, aca restamos al vat amount
                # lo que seria exento y no gravado
                imp_neto = str("%.2f" % abs(
                    inv.vat_base_amount - inv.vat_untaxed - inv.vat_exempt_amount))
            else:
                # tomado de la v9
                imp_neto = str("%.2f" % abs(inv.amount_untaxed))

            _logger.info("===================================================")
            _logger.info('doc afip code %s' % doc_afip_code)
            _logger.info('imp tot conc (0) %s' % imp_tot_conc)
            _logger.info('imp neto         %s' % imp_neto)
            ## wsfe_monotributo_fix

            imp_iva = str("%.2f" % abs(inv.vat_amount))
            imp_subtotal = str("%.2f" % abs(inv.amount_untaxed))
            imp_trib = str("%.2f" % abs(inv.other_taxes_amount))
            imp_op_ex = str("%.2f" % abs(inv.vat_exempt_amount))
            moneda_id = inv.currency_id.afip_code
            moneda_ctz = inv.currency_rate
            # moneda_ctz = str(inv.company_id.currency_id.compute(
            # 1., inv.currency_id))

            # # foreign trade data: export permit, country code, etc.:
            if inv.afip_incoterm_id:
                incoterms = inv.afip_incoterm_id.afip_code
                incoterms_ds = inv.afip_incoterm_id.name
            else:
                incoterms = incoterms_ds = None
            # por lo que verificamos, se pide permiso existente solo
            # si es tipo expo 1 y es factura (codigo 19), para todo el
            # resto pasamos cadena vacia
            if int(doc_afip_code) == 19 and tipo_expo == 1:
                # TODO investigar si hay que pasar si ("S")
                permiso_existente = "N"
            else:
                permiso_existente = ""
            obs_generales = inv.comment
            if inv.payment_term:
                forma_pago = inv.payment_term.name
                obs_comerciales = inv.payment_term.name
            else:
                forma_pago = obs_comerciales = None
            idioma_cbte = 1     # invoice language: spanish / español

            # customer data (foreign trade):
            nombre_cliente = commercial_partner.name
            # If argentinian and cuit, then use cuit
            if country.code == 'AR' and tipo_doc == 80 and nro_doc:
                id_impositivo = nro_doc
                cuit_pais_cliente = None
            # If not argentinian and vat, use vat
            elif country.code != 'AR' and commercial_partner.vat:
                id_impositivo = commercial_partner.vat[2:]
                cuit_pais_cliente = None
            # else use cuit pais cliente
            else:
                id_impositivo = None
                if commercial_partner.is_company:
                    cuit_pais_cliente = country.cuit_juridica
                else:
                    cuit_pais_cliente = country.cuit_fisica

            domicilio_cliente = " - ".join([
                                commercial_partner.name or '',
                                commercial_partner.street or '',
                                commercial_partner.street2 or '',
                                commercial_partner.zip or '',
                                commercial_partner.city or '',
            ])
            pais_dst_cmp = commercial_partner.country_id.afip_code

            # create the invoice internally in the helper
            if afip_ws == 'wsfe':
                ws.CrearFactura(
                    concepto, tipo_doc, nro_doc, doc_afip_code, pos_number,
                    cbt_desde, cbt_hasta, imp_total, imp_tot_conc, imp_neto,
                    imp_iva,
                    imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago,
                    fecha_serv_desde, fecha_serv_hasta,
                    moneda_id, moneda_ctz
                )
            elif afip_ws == 'wsmtxca':
                ws.CrearFactura(
                    concepto, tipo_doc, nro_doc, doc_afip_code, pos_number,
                    cbt_desde, cbt_hasta, imp_total, imp_tot_conc, imp_neto,
                    imp_subtotal,   # difference with wsfe
                    imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago,
                    fecha_serv_desde, fecha_serv_hasta,
                    moneda_id, moneda_ctz,
                    obs_generales   # difference with wsfe
                )
            elif afip_ws == 'wsfex':
                ws.CrearFactura(
                    doc_afip_code, pos_number, cbte_nro, fecha_cbte,
                    imp_total, tipo_expo, permiso_existente, pais_dst_cmp,
                    nombre_cliente, cuit_pais_cliente, domicilio_cliente,
                    id_impositivo, moneda_id, moneda_ctz, obs_comerciales,
                    obs_generales, forma_pago, incoterms,
                    idioma_cbte, incoterms_ds
                )

            # TODO ver si en realidad tenemos que usar un vat pero no lo
            # subimos
            if afip_ws != 'wsfex':
                for vat in inv.vat_tax_ids:
                    # we dont send no gravado y exento
                    if vat.tax_code_id.afip_code in [1, 2]:
                        continue
                    _logger.info('Adding VAT %s' % vat.tax_code_id.name)
                    # use instaed of "base_x" so it is not converted to
                    # company currency
                    ws.AgregarIva(
                        vat.tax_code_id.afip_code,
                        "%.2f" % abs(vat.base),
                        "%.2f" % abs(vat.amount),
                    )
                for tax in inv.not_vat_tax_ids:
                    _logger.info('Adding TAX %s' % tax.tax_code_id.name)
                    ws.AgregarTributo(
                        tax.tax_code_id.application_code,
                        tax.tax_code_id.name,
                        "%.2f" % abs(tax.base),
                        # como no tenemos la alicuota pasamos cero, en v9
                        # podremos pasar la alicuota
                        0,
                        "%.2f" % abs(tax.amount),
                    )

            CbteAsoc = inv.get_related_invoices_data()
            if CbteAsoc:
                ws.AgregarCmpAsoc(
                    CbteAsoc.afip_document_class_id.afip_code,
                    CbteAsoc.point_of_sale,
                    CbteAsoc.invoice_number,
                )

            # analize line items - invoice detail
            # wsfe do not require detail
            if afip_ws != 'wsfe':
                for line in inv.invoice_line:
                    codigo = line.product_id.code
                    # unidad de referencia del producto si se comercializa
                    # en una unidad distinta a la de consumo
                    if not line.uos_id.afip_code:
                        raise Warning(_('Not afip code con producto UOM %s' % (
                            line.uos_id.name)))
                    cod_mtx = line.uos_id.afip_code
                    ds = line.name
                    qty = line.quantity
                    umed = line.uos_id.afip_code
                    precio = line.price_unit
                    importe = line.price_subtotal
                    # calculamos bonificacion haciendo teorico menos importe
                    bonif = line.discount and (precio * qty - importe) or None
                    if afip_ws == 'wsmtxca':
                        if not line.product_id.uom_id.afip_code:
                            raise Warning(_('Not afip code con producto UOM %s' % (
                                line.product_id.uom_id.name)))
                        u_mtx = line.product_id.uom_id.afip_code or line.uos_id.afip_code
                        if inv.invoice_id.type in ('out_invoice', 'in_invoice'):
                            iva_id = line.vat_tax_ids.tax_code_id.afip_code
                        else:
                            iva_id = line.vat_tax_ids.ref_tax_code_id.afip_code
                        vat_taxes_amounts = line.vat_tax_ids.compute_all(
                            line.price_unit, line.quantity,
                            product=line.product_id,
                            partner=inv.partner_id)
                        imp_iva = vat_taxes_amounts[
                            'total_included'] - vat_taxes_amounts['total']
                        ws.AgregarItem(
                            u_mtx, cod_mtx, codigo, ds, qty, umed,
                            precio, bonif, iva_id, imp_iva, importe + imp_iva)
                    elif afip_ws == 'wsfex':
                        ws.AgregarItem(
                            codigo, ds, qty, umed, precio, importe,
                            bonif)

            # Request the authorization! (call the AFIP webservice method)
            vto = None
            msg = False
            try:
                if afip_ws == 'wsfe':
                    ws.CAESolicitar()
                    vto = ws.Vencimiento
                elif afip_ws == 'wsmtxca':
                    ws.AutorizarComprobante()
                    vto = ws.Vencimiento
                elif afip_ws == 'wsfex':
                    ws.Authorize(inv.id)
                    vto = ws.FchVencCAE
            except SoapFault as fault:
                msg = 'Falla SOAP %s: %s' % (
                    fault.faultcode, fault.faultstring)
            except Exception, e:
                msg = e
            except Exception:
                if ws.Excepcion:
                    # get the exception already parsed by the helper
                    msg = ws.Excepcion
                else:
                    # avoid encoding problem when raising error
                    msg = traceback.format_exception_only(
                        sys.exc_type,
                        sys.exc_value)[0]
            if msg:
                raise Warning(_('AFIP Validation Error. %s' % msg))

            msg = u"\n".join([ws.Obs or "", ws.ErrMsg or ""])
            if not ws.CAE or ws.Resultado != 'A':
                raise Warning(_('AFIP Validation Error. %s' % msg))
            # TODO ver que algunso campos no tienen sentido porque solo se
            # escribe aca si no hay errores
            _logger.info('CAE solicitado con exito. CAE: %s. Resultado %s' % (
                ws.CAE, ws.Resultado))
            inv.write({
                'afip_auth_mode': 'CAE',
                'afip_auth_code': ws.CAE,
                'afip_auth_code_due': vto,
                'afip_result': ws.Resultado,
                'afip_message': msg,
                'afip_xml_request': ws.XmlRequest,
                'afip_xml_response': ws.XmlResponse,
            })
