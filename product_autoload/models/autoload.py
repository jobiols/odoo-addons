# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class AutoloadMgr(models.Model):
    """ Administra la carga de datos en el sistema
    """

    name = fields.Char()

