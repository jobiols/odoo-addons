# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    export_perception = fields.Boolean(
        compute='_compute_perception',
        default=False,
        readonly=True,
        store=True,
        help='Marca la factura si tiene percepciones'
    )

    @api.multi
    @api.depends('tax_line_ids')
    def _compute_perception(self):
        for inv in self:
            for tax in inv.tax_line_ids.filtered(
                lambda r: r.tax_id.tax_group_id.type == 'perception'):
                inv.export_perception = True

    @api.multi
    def write(self, vals):
        self.compute_perceptions(vals)
        return super(AccountInvoice, self).write(vals)

    def compute_perceptions(self, vals):
        """ Calcular percepciones.
            agrega el impuesto de percepcion si la alicuota != 0
            solo para facturas de venta.
        """
        invoice_id = self.ensure_one()
        # si es una factura de compra no hay que hacerle percepciones
        if invoice_id.type == 'in_invoice':
            return

        # si la fecha es false poner la fecha de hoy
        if invoice_id.date_invoice:
            date_invoice = invoice_id.date_invoice
        else:
            date_invoice = fields.Date.context_today(self)
        ctx = {
            'date_invoice': date_invoice,
            'invoice_company': invoice_id.company_id
        }

        # obtener la alicuota para este partner, buscarla en base de datos o
        # si no la tengo consultar el ws de ARBA
        _ = invoice_id.partner_id.with_context(ctx)
        perception = _.get_arba_alicuota_percepcion()

        # si la alicuota es cero termina sin hacer nada
        if not perception:
            return

        tax_obj = self.env['account.tax']
        invoice_tax_obj = self.env['account.invoice.tax']

        # obtener los impuestos de percepcion FUERZO SOLO EL DE IIBB
        tax_ids = tax_obj.search([('type_tax_use', '=', 'sale'),
                                  ('tax_group_id.type', '=', 'perception'),
                                  ('name', 'like', '%IIBB%')])

        # Ver si ya tiene alguna una percepcion, si es asi hay que borrarla
        # porque pueden haber modificado la factura y debe ser recalculada.
        # salvo que sea manual, entonces no la tocamos.
        invoice_tax_obj.search(
            [('invoice_id', '=', invoice_id.id),
             ('manual', '=', False),
             ('tax_id.tax_group_id.type', '=', 'perception')]).unlink()

        base = invoice_id.amount_untaxed

        # Si la base supera el minimo no imponible no agregar impuesto
        if base < tax_ids.withholding_non_taxable_minimum:
            return

        for tax_id in tax_ids:
            res = tax_id.with_context(ctx).compute_all(
                base, partner=invoice_id.partner_id)
            tax = res['taxes'][0]
            val = {
                'invoice_id': invoice_id.id,
                'name': tax_id.name,
                'tax_id': tax_id.id,
                'amount': base * perception,
                'manual': False,
                'sequence': 99,
                'account_analytic_id': False,
                'account_id': invoice_id.type in (
                    'out_invoice', 'in_invoice') and (
                                  tax['account_id'] or False) or (
                                  tax['refund_account_id'] or False),
            }
            a = self.env['account.invoice.tax'].create(val)
            a.tax_id.compute_all(base, partner=invoice_id.partner_id)

    """
    def get_taxes_values(self):
        import wdb;wdb.set_trace()
        tax_grouped = super(AccountInvoice,self).get_taxes_values()

        invoice_id = self.ensure_one()
        tax_obj = self.env['account.tax']
        # obtener los impuestos de percepcion FUERZO SOLO EL DE IIBB
        tax_ids = tax_obj.search([('type_tax_use', '=', 'sale'),
                                  ('tax_group_id.type', '=', 'perception'),
                                  ('name', 'like', '%IIBB%')])

        taxes = tax_ids.compute_all(invoice_id.amount_untaxed, partner=invoice_id.partner_id)['taxes']
        for tax in taxes:
            val = {
                'invoice_id': invoice_id.id,
                'name': tax['name'],
                'tax_id': tax['id'],
                'amount': 2,
                'manual': False,
                'sequence': 99,
                'account_analytic_id': False,
                'account_id': invoice_id.type in (
                    'out_invoice', 'in_invoice') and (
                                  tax['account_id'] or False) or (
                                  tax['refund_account_id'] or False),
            }
            key = str(tax['id']) + str(self.id) + str(tax.get('analytic'))
            if key not in tax_grouped:
                tax_grouped[key] = val
            else:
                tax_grouped[key]['amount'] += val['amount']
                tax_grouped[key]['base'] += val['base']

        return tax_grouped
        """