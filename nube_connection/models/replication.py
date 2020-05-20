# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api


class NubeReplication(models.Model):
    _name = 'nube.replication'

    product_id = fields.Many2one(
        'product.product',
        ondelete='cascade',
        required=True
    )
    published = fields.Boolean(
        related='product_id.do_published'
    )

    def new_record(self, id_product):
        """ Agrega un registro para replicar pero sin repetirlo
        """
        replic_obj = self.env['nube.replication']
        rec = replic_obj.search([('product_id', '=', id_product)])
        if not rec:
            rec.create({'product_id': id_product})
