# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class NubeReplication(models.Model):
    _name = 'nube.replication'

    model = fields.Char(

    )
    id_rep = fields.Integer(

    )

    @api.multi
    def new_record(self, model, id_rep):
        """ Agrega un registro para replicar pero sin repetirlo
        """
        if not self.search([('model', '=', model),
                            ('id_rep', '=', id_rep)]):
            self.create({
                'model': model,
                'id_rep': id_rep
            })
