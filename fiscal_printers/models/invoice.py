# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning
import os
import logging
import time
import os.path

_logger = logging.getLogger(__name__)

try:
    from pyfiscalprinter.controlador import PyFiscalPrinter
except (ImportError, IOError) as err:
    _logger.debug(err)


class Invoice(models.Model):
    _inherit = 'account.invoice'

    n_factura_fiscal = fields.Char(
        string=u"Nº Comprobante Fiscal",
        size=20,
        readonly=True
    )

    def invoice_validate(self):
        res = super(Invoice, self).invoice_validate()

        # si el journal no es fiscal termino aca
        if not self.journal_id and self.journal_id.is_fiscal:
            return res

        fiscal = PyFiscalPrinter()

        marca = 'epson'
        modelo = 'tm-220-af'
        puerto = 1045
        equipo = '192.168.0.57'

        ok = fiscal.Conectar(marca=marca, modelo=modelo, puerto=puerto,
                             equipo=equipo)
        if not ok:
            raise Warning(fiscal.Excepcion)

        _logger.info('Imprimiendo ticket fiscal')

    @api.multi
    def invoice_validate1(self):
        res = super(Invoice, self).invoice_validate()

        if res:
            if self.state == 'open' and self.journal_id and self.journal_id.is_fiscal:
                #dirpath = '/opt/odoo/extra-addons/avalon/fiscal/Pto01/'
                dirpath = self.journal_id.dir_fiscal
                rel_filepath = "{0}.txt".format(self.display_name)
                abs_filepath = os.path.abspath(os.path.join(dirpath, rel_filepath))

                _logger.info("ENTRO:" + abs_filepath)

                # CODIGOS DE IVA
                #IVA Responsable Inscripto   1
                #IVA Responsable Inscripto Factura M 1FM
                #IVA Responsable no Inscripto    2
                #IVA no Responsable  3
                #IVA Sujeto Exento   4
                #Consumidor Final    5
                #Responsable Monotributo 6
                #Sujeto no Categorizado  7
                #Proveedor del Exterior  8
                #Cliente del Exterior    9
                #IVA Liberado – Ley Nº 19.640    10
                #IVA Responsable Inscripto – Agente de Percepción    11
                #Pequeño Contribuyente Eventual  12
                #Monotributista Social   13
                #Pequeño Contribuyente Eventual Social   14

                #Cat IVA de la EMPRESA
                catemp_iva = self.company_id.afip_responsability_type_id.code

                #Cat IVA del COMPRADOR
                catcli_iva = self.afip_responsability_type_id.code

                if catcli_iva == '1':
                    rfiva = 'I'
                elif catcli_iva == '1FM':
                    rfiva = 'I'
                elif catcli_iva == '2':
                    rfiva = 'N'
                elif catcli_iva == '3':
                    rfiva = 'A'
                elif catcli_iva == '4':
                    rfiva = 'E'
                elif catcli_iva == '5':
                    rfiva = 'C'
                elif catcli_iva == '6':
                    rfiva = 'M'
                elif catcli_iva == '7':
                    rfiva = 'T'
                elif catcli_iva == '11':
                    rfiva = 'I'
                elif catcli_iva == '12':
                    rfiva = 'V'
                elif catcli_iva == '13':
                    rfiva = 'S'
                elif catcli_iva == '14':
                    rfiva = 'W'
                else:
                    rfiva = 'C'

                #COMPRADOR tipo de documento DNI,CUIT,CUIL
                tdcli = self.partner_id.main_id_category_id.code
                # CUIT, CUIL, CDI, LE, LC, CIe, DNI, Sigd, 

                if tdcli == 'CUIT':
                    tdcli_code = 'C'
                elif tdcli == 'CUIL':
                    tdcli_code = 'L'
                elif tdcli == 'LE':
                    tdcli_code = '0'
                elif tdcli == 'LC':
                    tdcli_code = '1'
                elif tdcli == 'DNI':
                    tdcli_code = '2'
                elif tdcli == 'CDI':
                    tdcli_code = '4'
                elif tdcli == 'CIe':
                    tdcli_code = '3'
                else:
                    tdcli_code = ' '

                letra_doc = self.journal_document_type_id.document_type_id.document_letter_id.name
                #A B C ...

                tipo_doc = self.journal_document_type_id.document_type_id.internal_type
                # invoice, debit_note, credit_note, ticket,

                with open(abs_filepath, "w") as file:
                    if tipo_doc == 'credit_note':
                    # NOTA DE CREDITO
                        #Datos del Comprador
                        file.write("b{0}{1}{2}{3}{4}\n".format(self.partner_id.name.encode('utf-8')[:30],
                                                            self.partner_id.main_id_number,
                                                            rfiva,
                                                            tdcli_code,
                                                             self.partner_id.street[:40] if self.partner_id.street else ""  ))

                        #Set EmbarkNumber
                        file.write("{0}1Facturas\n".format(chr(147) ))

                        #Abro comprobante DNFH
                        tnc = 'S'
                        if letra_doc == 'A':
                            tnc = 'R'
                        file.write("{0}{1}T1\n".format(chr(128),tnc))

                        #Productos
                        for det in self.invoice_line_ids :
                            lista_iva = det.invoice_line_tax_ids.filtered(lambda record: record.name.find("IVA") > -1)
                            iva = lista_iva[0] if lista_iva else False
                            #nombre,monto,cantidad,iva
                            if det.price_unit >= 0:
                                file.write("B{0}{1}{2}{3}M0.00B\n".format(det.name.encode('utf-8')[:20],
                                                                            det.quantity,
                                                                            round(det.price_unit, 2),
                                                                            iva.amount))
                            else:
                                #Descuento General
                                file.write("m{0}{1}{2}m0.00BB\n".format(det.name.encode('utf-8')[:20],
                                                                            round(det.price_unit*-1, 2),
                                                                            iva.amount))

                        # Percepciones
                        for det in self.tax_line_ids :
                            if det.name.find('Perc') >= 0:
                                file.write("`{0}{1}{2}\n".format('**.**',
                                    det.name.encode('utf-8')[:20],
                                    round(det.amount, 2)))

                        #file.write("CPSubtotal0\n")
                        #file.write("DSu pago{0}T0\n".format(round(self.amount_total,2)))
                        #Cierre DNFH
                        file.write("{0}1\n".format(chr(129)))

                    #***********************************************************************************************

                    if tipo_doc in 'invoice debit_note':
                    # FACTURAS y NOTA DEBITO
                        #Datos del Comprador
                        file.write("b{0}{1}{2}{3}{4}\n".format(self.partner_id.name.encode('utf-8')[:30],
                                                            self.partner_id.main_id_number,
                                                            rfiva,
                                                            tdcli_code,
                                                             self.partner_id.street[:40] if self.partner_id.street else ""  ))

                        #Abro comprobante
                        tci = 'T'
                        if tipo_doc == 'invoice':
                            tci = 'B'
                            if letra_doc == 'A':
                                tci = 'A'

                        if tipo_doc == 'debit_note':
                            tci = 'E'
                            if letra_doc == 'A':
                                tci = 'D'

                        file.write("@{0}T\n".format(tci))

                        #Imprimo fact interna de ODOO
                        #file.write("A{0}\n".format(self.display_name))

                        #Productos
                        for det in self.invoice_line_ids :
                            lista_iva = det.invoice_line_tax_ids.filtered(lambda record: record.name.find("IVA") > -1)
                            iva = lista_iva[0] if lista_iva else False
                            #nombre,monto,cantidad,iva
                            if det.price_unit >= 0:
                                file.write("B{0}{1}{2}{3}M0.00B\n".format(det.name.encode('utf-8')[:20],
                            												det.quantity,
                                                                            round(det.price_unit, 2),
                                                                            iva.amount))
                            else:
                                #Descuento General
                                file.write("m{0}{1}{2}m0.00BB\n".format(det.name.encode('utf-8')[:20],
                                                                            round(det.price_unit*-1, 2),
                                                                            iva.amount))

                        # Percepciones
                        for det in self.tax_line_ids :
                            if det.name.find('Perc') >= 0:
                                file.write("`{0}{1}{2}\n".format('**.**',
                                    det.name.encode('utf-8')[:20],
                                    round(det.amount, 2)))

                        file.write("CPSubtotal0\n")
                        file.write("DSu pago{0}T0\n".format(round(self.amount_total,2)))
                        #Cierre Doc Fiscal
                        file.write("E")

                #*******************************************************

                #Obtengo Nro comprobante de la FISCAL
                arch = abs_filepath.replace('.txt','.ans')

                ncomp = '0'
                for i in range(4):
                    time.sleep(3)
                    if os.path.isfile(arch):
                        with open(arch) as fp:
                            lines = fp.read().splitlines()
                            ncomp = lines[-1]
                        break

                cok = '0000000010000000|0000011000000000|'
                if ncomp[:34] == cok:
                    #_logger.info("Nro Comprobante:" + ncomp[-(len(ncomp)-34):])
                    ncomp = ncomp[-(len(ncomp)-34):].zfill(8)
                    nff = self.display_name
                    _logger.info(nff[:len(nff)-8] + ncomp)

                    self.n_factura_fiscal = nff[:len(nff)-8] + ncomp
                else:
                    _logger.info("Nro Comprobante:  ERROR!!!!!!")
                    self.n_factura_fiscal = "Comp: ERROR!"

        return res