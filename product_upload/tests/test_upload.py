# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp.tests import common
import os
import openpyxl

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
#   oe -Q product_upload -c iomaq -d iomaq_test_product_upload
#

DECKER_0 = [{
    'default_code': 'D25811K-AR-DECKER',
    'currency': u'ARS',
    'cost': 9490.76,
    'price': 10000.0,
    'name': u'17 MM HEX DEDICATED CHIPPING HAMMER',
    'purchase_tax': 0.155,
    'sale_tax': 0.155,
    'barcode': 885911484848L,
    'meli': u'MELICODE123',
    'parent': False,
}]

EINHELL_0 = [{
    'default_code': '4502015-EINHELL',
    'currency': u'ARS',
    'cost': 9490.76,
    'price': 10000.0,
    'name': u'Accesorio - Discos para TE-XC 110',
    'purchase_tax': 0.21,
    'sale_tax': 0.21,
    'barcode': False,
    'meli': False,
    'parent': '4502015',
}]


class TestProductUploadProduct(common.TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """

    def setUp(self):
        super(TestProductUploadProduct, self).setUp()
        self.wizard_obj = self.env['product_upload.import_worksheet']

        log_obj = self.env['product_upload.log']
        self.wizard_obj.log = log_obj.create({})

    @staticmethod
    def get_filename(nro):
        path = os.path.dirname(os.path.realpath(__file__))
        return path + '/products_{}.xlsx'.format(nro)

    def get_ws(self, nro):
        return openpyxl.load_workbook(filename=self.get_filename(nro),
                                      read_only=True,
                                      data_only=True)

    def test_01_(self):
        """ cargar una linea del primer proveedor -----------------------------
        """
        data = self.wizard_obj.read_data(self.get_ws(0)['B&D'])
        self.assertEqual(data[0]['default_code'], DECKER_0[0]['default_code'])
        self.assertEqual(data[0]['currency'], DECKER_0[0]['currency'])
        self.assertEqual(data[0]['cost'], DECKER_0[0]['cost'])
        self.assertEqual(data[0]['price'], DECKER_0[0]['price'])
        self.assertEqual(data[0]['name'], DECKER_0[0]['name'])
        self.assertEqual(data[0]['purchase_tax'], DECKER_0[0]['purchase_tax'])
        self.assertEqual(data[0]['sale_tax'], DECKER_0[0]['sale_tax'])
        self.assertEqual(data[0]['barcode'], DECKER_0[0]['barcode'])
        self.assertEqual(data[0]['meli'], DECKER_0[0]['meli'])
        self.assertEqual(data[0]['parent'], False)

    def test_02_(self):
        """ cargar una linea del segundo proveedor ----------------------------
        """
        data = self.wizard_obj.read_data(self.get_ws(0)['EINHELL'])
        self.assertEqual(data[0]['default_code'], EINHELL_0[0]['default_code'])
        self.assertEqual(data[0]['currency'], EINHELL_0[0]['currency'])
        self.assertEqual(data[0]['cost'], EINHELL_0[0]['cost'])
        self.assertEqual(data[0]['price'], EINHELL_0[0]['price'])
        self.assertEqual(data[0]['name'], EINHELL_0[0]['name'])
        self.assertEqual(data[0]['purchase_tax'], EINHELL_0[0]['purchase_tax'])
        self.assertEqual(data[0]['sale_tax'], EINHELL_0[0]['sale_tax'])
        self.assertEqual(data[0]['barcode'], EINHELL_0[0]['barcode'])
        self.assertEqual(data[0]['meli'], EINHELL_0[0]['meli'])
        self.assertEqual(data[0]['parent'], '4502015')

    def test_03_(self):
        """ Cargar los productos y verificar que esten bien
        """
        self.wizard_obj.process_tmp_file(self.get_filename(0))
        self.assertEqual(self.wizard_obj.log.state, 'done')

        prod_obj = self.env['product.template']

        domain = [('default_code', '=', DECKER_0[0]['default_code'])]
        decker = prod_obj.search(domain)
        self.assertEqual(decker.default_code, DECKER_0[0]['default_code'])
        self.assertEqual(decker.force_currency_id.name, False)
        self.assertEqual(decker.standard_price, DECKER_0[0]['cost'])
        self.assertEqual(decker.list_price, DECKER_0[0]['price'])
        self.assertEqual(decker.name, DECKER_0[0]['name'])
        self.assertEqual(decker.taxes_id[0].amount,
                         DECKER_0[0]['sale_tax'] * 100)
        self.assertEqual(decker.supplier_taxes_id[0].amount,
                         DECKER_0[0]['purchase_tax'] * 100)

        self.assertEqual(decker.barcode_ids[0].name,
                         str(DECKER_0[0]['barcode']))
        self.assertEqual(decker.meli_code, DECKER_0[0]['meli'])

        domain = [('default_code', '=', EINHELL_0[0]['default_code'])]
        einhell = prod_obj.search(domain)
        self.assertEqual(einhell.default_code, EINHELL_0[0]['default_code'])
        self.assertEqual(einhell.force_currency_id.name, False)
        self.assertEqual(einhell.standard_price, EINHELL_0[0]['cost'])
        self.assertEqual(einhell.list_price, EINHELL_0[0]['price'])
        self.assertEqual(einhell.name, EINHELL_0[0]['name'])
        self.assertEqual(einhell.taxes_id[0].amount,
                         EINHELL_0[0]['sale_tax'] * 100)
        self.assertEqual(einhell.supplier_taxes_id[0].amount,
                         EINHELL_0[0]['purchase_tax'] * 100)
        self.assertEqual(einhell.barcode_ids or False, False)
        self.assertEqual(einhell.meli_code, False)
        self.assertEqual(einhell.parent_price_product, '4502015')

    def test_04_(self):
        """ Archivo con multiples productos
        """
        self.wizard_obj.process_tmp_file(self.get_filename(0))
        self.assertEqual(self.wizard_obj.log.state, 'done')
