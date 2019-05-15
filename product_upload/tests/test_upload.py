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
    'parent': 'B3423',
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
        self.prod_obj = self.env['product.template']

        # Agregar al admin al grupo de crear productos para que funcione
        # el test.
        create_prod_group = self.env['res.groups'].search(
            [('name', '=', 'Create products manually')])
        admin = self.env['res.users'].search([('id', '=', 1)])
        create_prod_group.users += admin

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
        data = self.wizard_obj.read_data(self.get_ws(0)['B&D'])[0]
        self.assertEqual(data['default_code'], u'D25811K-AR-DECKER')
        self.assertEqual(data['currency'], u'ARS')
        self.assertEqual(data['cost'], 9490.76)
        self.assertEqual(data['price'], 10000.0)
        self.assertEqual(data['name'], u'17 MM HEX DEDICATED CHIPPING HAMMER')
        self.assertEqual(data['purchase_tax'], 0.155)
        self.assertEqual(data['sale_tax'], 0.155)
        self.assertEqual(data['barcode'], u'885911484848')
        self.assertEqual(data['meli'], u'MELICODE123')
        self.assertEqual(data['parent'], None)

    def test_02_(self):
        """ cargar una linea del segundo proveedor ----------------------------
        """
        data = self.wizard_obj.read_data(self.get_ws(0)['EINHELL'])[0]
        self.assertEqual(data['default_code'], u'4502015-EINHELL')
        self.assertEqual(data['currency'], u'ARS')
        self.assertEqual(data['cost'], 9490.76)
        self.assertEqual(data['price'], 10000.0)
        self.assertEqual(data['name'], u'Accesorio - Discos para TE-XC 110')
        self.assertEqual(data['purchase_tax'], 0.21)
        self.assertEqual(data['sale_tax'], 0.21)
        self.assertEqual(data['barcode'], None)
        self.assertEqual(data['meli'], None)
        self.assertEqual(data['parent'], 'B3423')

    def test_03_(self):
        """ Cargar los productos y verificar que esten bien
        """
        self.wizard_obj.process_tmp_file(self.get_filename(0))
        self.assertEqual(self.wizard_obj.log.state, 'done')

        prod_obj = self.env['product.template']
        domain = [('default_code', '=', u'D25811K-AR-DECKER')]
        decker = prod_obj.search(domain)
        self.assertEqual(decker.default_code, u'D25811K-AR-DECKER')
        self.assertEqual(decker.force_currency_id.name, False)
        self.assertEqual(decker.standard_price, 9490.76)
        self.assertEqual(decker.list_price, 10000.0)
        self.assertEqual(decker.name, u'17 MM HEX DEDICATED CHIPPING HAMMER')
        self.assertEqual(decker.taxes_id[0].amount, 15.5)
        self.assertEqual(decker.supplier_taxes_id[0].amount, 15.5)
        self.assertEqual(decker.barcode_ids[0].name, u'885911484848')
        self.assertEqual(decker.meli_code, u'MELICODE123')

        domain = [('default_code', '=', EINHELL_0[0]['default_code'])]
        einhell = prod_obj.search(domain)
        self.assertEqual(einhell.default_code, u'4502015-EINHELL')
        self.assertEqual(einhell.force_currency_id.name, False)
        self.assertEqual(einhell.standard_price, 9490.76)
        self.assertEqual(einhell.list_price, 10000.0)
        self.assertEqual(einhell.name, u'Accesorio - Discos para TE-XC 110')
        self.assertEqual(einhell.taxes_id[0].amount, 21)
        self.assertEqual(einhell.supplier_taxes_id[0].amount, 21)
        self.assertEqual(einhell.barcode_ids or False, False)
        self.assertEqual(einhell.meli_code, False)
        self.assertEqual(einhell.parent_price_product, 'B3423')

    def test_04_(self):
        """ terminar el proceso con done
        """
        self.wizard_obj.process_tmp_file(self.get_filename(0))
        self.assertEqual(self.wizard_obj.log.state, 'done')

    def test_05_(self):
        """ planilla con none en default code, no carga la linea
        """
        self.wizard_obj.process_tmp_file(self.get_filename(1))
        self.assertEqual(self.wizard_obj.log.state, 'done')

    def test_06_(self):
        """ Error por falta de campos requeridos
        """
        self.wizard_obj.process_tmp_file(self.get_filename(2))
        domain = [('default_code', '=', '1077-EINHELL')]
        einhell = self.prod_obj.search(domain)
        self.assertEqual(einhell.default_code, u'1077-EINHELL')

        self.wizard_obj.process_tmp_file(self.get_filename(2))
        self.assertEqual(self.wizard_obj.log.state, 'error')

    def test_07_(self):
        """ Chequear trimming del codigo de producto
        """
        import wdb;wdb.set_trace()
        # el producto tiene un espacio despues del codigo
        self.wizard_obj.process_tmp_file(self.get_filename(3))
        # lo tiene que cargar sin el espacio
        domain = [('default_code', '=', '1077-EINHELL')]
        einhell = self.prod_obj.search(domain)
        self.assertEqual(einhell.default_code, u'1077-EINHELL')
