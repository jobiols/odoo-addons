# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division

from odoo.addons.business.models.business import Kpis
from odoo.tests.common import TransactionCase
from odoo.addons.business.models.business import _margin


#    Forma de correr el test
#    -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre (por ejemplo act_test)
#   vacia y con el modulo que se va a testear instalado (por ejemplo business).
#
#   El usuario admin tiene que tener password admin, Language English, Country
#   United States.
#
#   oe -Q product_upload_prices -c iomaq -d iomaq_test
#


class TestUpload(TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """
    print 'running test'