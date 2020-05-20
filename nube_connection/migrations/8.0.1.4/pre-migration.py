# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


def migrate(cr, version):
    """ Forzar recalculo de la columna
    """
    cr.execute(
        """
        delete from nube_replication
        """)
