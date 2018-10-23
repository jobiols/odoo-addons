# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import models, fields, api, _


class Log(models.Model):
    _description = "Log of product uploads"
    _name = 'product_upload.log'

    updated_products = fields.Integer(
    )
    created_products = fields.Integer(
    )
    errors = fields.Integer(
    )
    error_ids = fields.One2many(
        comodel_name="product_upload.error",
        inverse_name="log_id",
        string="Errors",
        readonly=True
    )
    state = fields.Selection(
        [('load', 'Load'),
         ('process', 'Process'),
         ('error', 'Error'),
         ('done', 'Done')],
        default="load"
    )

    @api.multi
    def name_get(self):
        ret = []
        for rec in self:
            name = _(u'Uploaded for {} on {}').format(rec.create_uid.name,
                                                      rec.create_date)
            ret.append((rec.id, name))
        return ret

    @api.multi
    def import_worksheet(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Worksheet',
            'res_model': 'product_upload.import_worksheet',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }
