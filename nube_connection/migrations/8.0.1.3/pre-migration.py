# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


def migrate(cr, version):
    """ Forzar recalculo de stock_match
    """
    cr.execute(
        """
        ALTER TABLE product_product
          DROP COLUMN stock_match
        """)
