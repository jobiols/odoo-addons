# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api, _
from openerp.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        """ No permitir la creacion de productos a cualquiera.
        """
        if self.env.user.has_group(
            'product_upload.group_product_create_users'):
            return super(ProductTemplate, self).create(vals)
        else:
            raise AccessError(_("You do not have permission to create "
                                "products, if you really need to create a "
                                "product, please contact a user who has "
                                "permissions."))


