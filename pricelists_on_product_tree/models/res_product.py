# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import models, fields, api
from lxml import etree


class ProductProduct(models.Model):
    _inherit = 'product.template'

    pricelist_1 = fields.Float(
        u'Precio 1',
        compute='_compute_prices'
    )
    pricelist_2 = fields.Float(
        u'Precio 2',
        compute='_compute_prices'
    )
    pricelist_3 = fields.Float(
        u'Precio 3',
        compute='_compute_prices'
    )

    @api.one
    @api.depends('standard_price')
    def _compute_prices(self):

        # traer las pricelist configuradas
        pricelists = self._get_pricelists()

        ppobj = self.env['product.pricelist']
        prices = ppobj.price_get(self.product_variant_ids.id, 1.0)

        for pricelist in pricelists:
            if pricelist == 'pricelist_1' and pricelists[pricelist]:
                self.pricelist_1 = prices[pricelists[pricelist].id]

            if pricelist == 'pricelist_2' and pricelists[pricelist]:
                self.pricelist_2 = prices[pricelists[pricelist].id]

            if pricelist == 'pricelist_3' and pricelists[pricelist]:
                self.pricelist_3 = prices[pricelists[pricelist].id]

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', context=None,
                        toolbar=False, submenu=False):
        """ Sobreescribimos fields_view_get para cambiar los nombres de los
            campos del tree view
        """
        result = super(ProductProduct, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if view_type == 'tree':
            # traer las pricelist configuradas
            pricelists = self._get_pricelists()

            doc = etree.XML(result['arch'])
            for field_name in pricelists:
                for node in doc.xpath("//field[@name="
                                      "'{}']".format(field_name)):
                    if pricelists[field_name]:
                        node.set('string', pricelists[field_name].name)
                    else:
                        node.set('invisible', '1')
                        node.set('modifiers',
                                 '{"readonly": true, "tree_invisible": true}')
            result['arch'] = etree.tostring(doc)

        return result

    def _get_pricelists(self):
        """ traer las tres listas de precio de la configuracion
        """
        # traigo dict con {fieldname: id} de las listas
        pricelist = self.env['sale.config.settings'].get_default_params(False)
        pricelist_obj = self.env['product.pricelist']

        # reemplazo el id por la pricelist y me traigo solo las que no son
        # false
        for field_name in pricelist:
            pricelist_id = pricelist[field_name]
            obj = pricelist_obj.search([('id', '=', pricelist_id)])
            pricelist[field_name] = obj if obj else False

        return pricelist
