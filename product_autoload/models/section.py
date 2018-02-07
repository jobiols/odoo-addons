# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class Section(models.Model):
    """ Una Seccion es un conjunto de rubros
    """
    _name = 'product_autoload.section'

    section_code = fields.Char(
        help="Code from bulonfer, not shown"
    )
    name = fields.Char(
        help="Name of section to show in category full name"
    )
    item_ids = fields.One2many(
        'product_autoload.item',
        'section_id')
