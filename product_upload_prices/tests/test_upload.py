# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp.tests import common

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
#   oe -Q product_upload_prices -c iomaq -d product_upload_prices_test
#


class TestProductUploadPrices(common.TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """
    def setUp(self):
        super(TestProductUploadPrices, self).setUp()
        self.upload_obj = self.env['product_upload_prices.upload_prices']

    def test_01_(self):
        self.assertEqual(1, 2)

