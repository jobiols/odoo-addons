# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


def migrate(cr, version):
    cr.execute(
        """
        INSERT INTO curso_woo_categ_product_product_rel
        (
          product_product_id,
          curso_woo_categ_id
        )
        SELECT
          id, woo_categ
        FROM
          product_product
        WHERE
          woo_categ is not null;
        """)
