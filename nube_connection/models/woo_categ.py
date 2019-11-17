# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import models, fields, api


class CursoWooCateg(models.Model):
    _name = 'curso.woo.categ'
    # esto hace que el name del registro sea path
    _rec_name = 'path'
    _order = 'woo_idx,slug'


    path = fields.Char(
            compute="get_path",
            store=True
    )

    nube_id = fields.Integer(
    )

    woo_ids = fields.Char(
            compute="get_woo_ids"
    )

    woo_idx = fields.Integer(
            compute="get_woo_idx",
            store=True
    )

    slug = fields.Char(
    )

    name = fields.Char(
    )

    parent = fields.Many2one(
            'curso.woo.categ',
            string="Parent"
    )
    published = fields.Boolean(
        'Publicado en tienda nube',
        help=u'Indica si se publica en tienda nube'
    )


    @api.multi
    def _path(self):
        for cat in self:
            if cat.parent:
                return u'{} / {} '.format(cat.parent._path(), cat.name)
            else:
                return cat.name

    @api.one
    @api.depends('parent', 'name')
    def get_path(self):
        self.path = self._path()

    @api.one
    def get_woo_ids(self):
        ids = []
        ids.append(self.nube_id)
        if self.parent:
            ids.append(self.parent.nube_id)
            if self.parent.parent:
                ids.append(self.parent.parent.nube_id)
        self.woo_ids = ids

    @api.one
    @api.depends('woo_ids')
    def get_woo_idx(self):
        ids = eval(self.woo_ids)
        self.woo_idx = len(ids)
