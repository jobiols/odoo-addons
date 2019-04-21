# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, api, _, SUPERUSER_ID
from openerp.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        """ No permitir la creacion de productos a cualquiera.
        """
        if self.env.user.id == SUPERUSER_ID or self.env.user.has_group(
                'product_create_restriction.group_product_create_users'):
            return super(ProductTemplate, self).create(vals)
        else:
            raise AccessError(_("You do not have permission to create "
                                "products, if you really need to create a "
                                "product, please contact a user who has "
                                "permissions."))
