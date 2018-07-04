# -*- coding: utf-8 -*-
# © 2012-2014 Guewen Baconnier (Camptocamp SA)
# © 2015 Roberto Lizana (Trey)
# © 2016 Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.osv import expression
import re


class ProductBarcode(models.Model):
    _name = 'product.barcode'
    _description = "List of Barcodes for a product."

    name = fields.Char(
        string='Barcode',
        required=True
    )
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.template',
        ondelete='cascade',
        required=True,
    )

    _sql_constraints = [
        ('uniq_barcode', 'unique(name)', "The barcode must be unique !"),
    ]

    @api.multi
    def add_barcode(self, product_id, barcode):
        """ add a new barcode if it does not exist
            if it exists with another product, fix it

        :param product_id: the product
        :param barcode: the barcode
        :return: none
        """
        ret = []
        # search for the barcode
        bc = self.search([('name', '=', barcode)])
        if bc:
            # check if it has the correct product and correct if necessary
            if bc.product_id.id != product_id.id:
                bc.product_id = product_id.id
                ret = ['barc_changed']
        else:
            # no barcode, then create it
            self.create({
                'product_id': product_id.id,
                'name': barcode
            })
            ret = ['barc_created']

        return ret


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many(
        comodel_name='product.barcode',
        inverse_name='product_id',
        string='Barcodes')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode_ids = fields.One2many(
        related='product_tmpl_id.barcode_ids'
    )

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):

        if context is None:
            context = {}
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            ids = []
            if operator in positive_operators:
                ids = self.search(cr, user,
                                  [('default_code', '=', name)] + args,
                                  limit=limit, context=context)
                if not ids:
                    ids = self.search(cr, user,
                                      [('barcode_ids.name', '=', name)] + args,
                                      limit=limit, context=context)
            if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                # Do not merge the 2 next lines into one single search, SQL
                # search performance would be abysmal on a database with
                # thousands of matching products, due to the huge merge+unique
                # needed for the OR operator (and given the fact that the
                # 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give
                # much better performance
                ids = self.search(cr, user,
                                  args + [('default_code', operator, name)],
                                  limit=limit, context=context)
                if not limit or len(ids) < limit:
                    # we may underrun the limit because of dupes in the
                    # results, that's fine
                    limit2 = (limit - len(ids)) if limit else False
                    ids += self.search(cr, user,
                                       args + [('name', operator, name),
                                               ('id', 'not in', ids)],
                                       limit=limit2, context=context)
            elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args + [
                    '&',
                    ('default_code', operator, name),
                    ('name', operator, name)], limit=limit, context=context)
            if not ids and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(cr, user, [
                        ('default_code', '=', res.group(2))
                    ] + args, limit=limit, context=context)
            # still no results, partner in context: search on supplier info as
            # last hope to find something
            if not ids and context.get('partner_id'):
                supplier_ids = self.pool['product.supplierinfo'].search(
                    cr, user, [
                        ('name', '=', context.get('partner_id')),
                        '|',
                        ('product_code', operator, name),
                        ('product_name', operator, name)
                    ], context=context)
                if supplier_ids:
                    ids = self.search(cr, user, [
                        ('product_tmpl_id.seller_ids', 'in',
                         supplier_ids)], limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result
