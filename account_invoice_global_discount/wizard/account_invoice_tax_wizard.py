##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountInvoiceDiscountWizard(models.TransientModel):
    _name = 'account.invoice.discount.wizard'
    _description = 'Account Invoice Discount Wizard'

    @api.model
    def _get_invoice(self):
        return self._context.get('active_id', False)

    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice',
        default=_get_invoice)

    discount = fields.Float(
        digits=dp.get_precision('Account'),
        required=True)

    amount_untaxed = fields.Float(

    )

    base_105 = fields.Float(
        string='Base IVA 10.5%',
        digits=dp.get_precision('Account'),
        required=True)

    base_21 = fields.Float(
        string='Base IVA 21%',
        digits=dp.get_precision('Account'),
        required=True)

    @api.onchange('invoice_id')
    def onchange_invoice(self):
        base_21 = base_105 = 0
        for line in self.invoice_id.invoice_line_ids:
            if line.invoice_line_tax_ids.amount == 21.0:
                base_21 += line.price_subtotal
            if line.invoice_line_tax_ids.amount == 10.5:
                base_105 += line.price_subtotal
        self.base_105 = base_105
        self.base_21 = base_21
        self.amount_untaxed = self.invoice_id.amount_untaxed

    invoice_type = fields.Selection(
        related='invoice_id.type', string='Invoice Type', readonly=True, )
    invoice_company_id = fields.Many2one(
        'res.company', string='Company',
        related='invoice_id.company_id', readonly=True, )

    @api.multi
    def confirm(self):
        if not self.invoice_id:
            return False

        tax_obj = self.env['account.tax']
        tax21 = tax_obj.search([('amount', '=', 21.0),
                                ('tax_group_id.tax', '=', 'vat'),
                                ('type_tax_use', '=', 'purchase')])
        tax105 = tax_obj.search([('amount', '=', 10.5),
                                 ('tax_group_id.tax', '=', 'vat'),
                                 ('type_tax_use', '=', 'purchase')])

        invoice = self.invoice_id
        acc_obj = self.env['account.account']
        acc_id = acc_obj.search([('code', '=', '4.1.01.02.010')])

        if self.base_21:
            val_21 = {
                'sequence': 99,
                'name': 'Descuento',
                'invoice_id': invoice.id,
                'account_id': acc_id.id,
                'price_unit': self._calc_discount_21(),
                'invoice_line_tax_ids': [(6, 0, [tax21.id])],
            }
            self.invoice_id.invoice_line_ids.create(val_21)

        if self.base_105:
            val_105 = {
                'sequence': 99,
                'name': 'Descuento',
                'invoice_id': invoice.id,
                'account_id': acc_id.id,
                'price_unit': self._calc_discount_105(),
                'invoice_line_tax_ids': [(6, 0, [tax105.id])],
            }
            self.invoice_id.invoice_line_ids.create(val_105)

    def _calc_discount_21(self):
        percent = self.discount / self.amount_untaxed
        return self.base_21 * -percent

    def _calc_discount_105(self):
        percent = self.discount / self.amount_untaxed
        return self.base_105 * -percent
