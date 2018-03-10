# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division

from openerp.tests.common import TransactionCase
from ..models.mappers import ProductMapper, SectionMapper, FamilyMapper, \
    ItemMapper, ProductCodeMapper

#    Forma de correr el test
#    -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben empezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre (por ejemplo
#   bulonfer_test) vacia y con el modulo que se va a testear instalado
#   (por ejemplo product_autoload).
#
#   El usuario admin tiene que tener password admin, Language English, Country
#   United States.
#
#   Correr el test con:
#
#   oe -Q product_autoload -c bulonfer -d bulonfer_test
#
#

import os


class TestBusiness(TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """

    def setUp(self):
        """ Este setup corre antes de cada método ---------------------------01
        """
        super(TestBusiness, self).setUp()
        # obtener el path al archivo de datos
        self._data_path = os.path.realpath(__file__)
        self._data_path = self._data_path.replace('tests/test_autoload.py',
                                                  'data/')
        self.env['ir.config_parameter'].set_param('data_path', self._data_path)

        self._vendor = self.env['res.partner'].search(
            [('name', 'like', 'Bulonfer')])

        self._supinfo = self.env['product.supplierinfo']

        self.env['res.partner'].create({'name': 'Bulonfer'})

    def test_00_all_mappers(self):
        Section = SectionMapper([u'1', u'Bulones'])
        self.assertEqual(Section.write_date, '')

        Family = FamilyMapper([u'SNP', u'SIN PAR'])
        self.assertEqual(Family.write_date, '')

        Item = ItemMapper([u'102', u'ARANDELA', u'Nacional', u'1', u'ARA'])
        self.assertEqual(Item.write_date, '')

        Product = ProductCodeMapper([u'106.32', u'106.32', u'50'])
        self.assertEqual(Product.write_date, '')

    def test_01_product_mapper(self):
        """ Chequear creacion de ProductMapper ------------------------------01
        """

        line = [
            '123456',
            'nombre-producto',
            'Descripción del producto',
            '500.22',
            '100',
            '200.50',
            '125.85',
            '100',
            '5',
            '102.7811.jpg',
            '60',
            '15.5',
            '001',
            '2018-25-01 13:10:55']

        prod = ProductMapper(line, self._data_path, self._vendor,
                             self._supinfo)
        self.assertEqual(prod.default_code, '123456')
        self.assertEqual(prod.name, 'nombre-producto')
        self.assertEqual(prod.description_sale, 'Descripción del producto')
        self.assertEqual(prod.standard_price, 500.22)
        self.assertEqual(prod.upv, 100)
        self.assertEqual(prod.weight, 200.50)
        self.assertEqual(prod.volume, 125.85)
        self.assertEqual(prod.wholesaler_bulk, 100)
        self.assertEqual(prod.retail_bulk, 5)
        self.assertEqual(prod.warranty, 60)
        self.assertEqual(prod.iva, 15.5)
        self.assertEqual(prod.item_code, '001')
        self.assertEqual(prod.write_date, '2018-25-01 13:10:55')

        val = {
            'wholesaler_bulk': 100,
            'retail_bulk': 5,
            'warranty': 60.0,
            'upv': 100,
            'name': 'nombre-producto',
            'weight': 200.5,
            'standard_price': 500.22,
            'volume': 125.85,
            'default_code': '123456',
            'write_date': '2018-25-01 13:10:55',
            'description_sale': 'Descripci\xc3\xb3n del producto'}

        val.update(prod.default_values())

        for item in val:
            self.assertEqual(prod.values(create=True)[item], val[item])

    def test_02_productcode(self):
        """ Chequear creacion de ProductCode --------------------------------02
        """
        line = [
            '003.0151-5/at',
            '171.003.0151.5',
            '1']

        prod = ProductCodeMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

        self.assertEqual(prod.barcode, '003.0151-5/at')
        self.assertEqual(prod.product_code, '171.003.0151.5')
        self.assertEqual(prod.uxb, 1)

        val = {
            'barcode': '003.0151-5/at',
            'product_code': '171.003.0151.5',
            'uxb': 1}

        for item in val:
            self.assertEqual(prod.values()[item], val[item])

    def test_03_(self):
        """ Chequear tipos de campo -----------------------------------------03
        """
        line = [
            u'1aa\xe11',
            'nombre-producto',
            'Descripción del producto',
            '7750082001169,7750082001169',
            '1000.52',
            '501',
            '200.50',
            '125.85',
            '601.AA.3157.jpg',
            '60',
            '21',
            '001',
            '2018-25-01 13:10:55']

        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_04_(self):
        """ Chequear tipos de campo currency -------------------------------004
        """
        line = [
            '123456789',
            'nombre-producto',
            'Descripción del producto',
            '7750082001169,7750082001169',
            '100a0.52',
            '501',
            '200.50',
            '125.85',
            '601.AA.3157.jpg',
            '60',
            '21',
            '001',
            '2018-25-01 13:10:55']

        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_05_(self):
        """ Chequear tipos de campo currency --------------------------------05
        """
        line = [
            '123456789',
            'nombre-producto',
            'Descripción del producto',
            '7750082001169,7750082001169',
            '1000.52',
            '500',
            '200q',
            '125.85',
            '601.AA.3157.jpg',
            '60',
            '21',
            '001',
            '2018-25-01 13:10:55']

        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_06_update_product(self):
        """ Chequear update de producto -------------------------------------06
        """
        # verificar create
        manager_obj = self.env['product_autoload.manager']
        prod_obj = self.env['product.template']
        manager_obj.run(send_mail=False)

        prod = prod_obj.search([('default_code', '=', '102.AF')])
        self.assertEqual(len(prod), 1, '102.AF')
        self.assertEqual(prod.item_code, '102')

        prod = prod_obj.search([('default_code', '=', '106.32')])
        self.assertEqual(len(prod), 1, '106.32')
        self.assertEqual(prod.item_code, '106')

        # verificar update

        manager_obj.run(send_mail=False)

        prod = prod_obj.search([('default_code', '=', '102.AF')])
        self.assertEqual(len(prod), 1, '102.AF')
        self.assertEqual(prod.item_code, '102')

        prod = prod_obj.search([('default_code', '=', '106.32')])
        self.assertEqual(len(prod), 1, '106.32')
        self.assertEqual(prod.item_code, '106')

    def test_7_barcodes(self):
        """ Testear que el unlink borra todo ---------------------------------7
        """
        # verificar create
        manager_obj = self.env['product_autoload.manager']
        prod_obj = self.env['product.template']
        manager_obj.run(send_mail=False)

        barcode_obj = self.env['product.barcode']
        for bc in barcode_obj.search([('product_id.name', '=', '102.7811')]):
            self.assertTrue(bc.barcode in ['5449000000996', '299999134500'])

    def test_8_categories(self):
        """ Testear actualizacion de categorias-------------------------------8
        """
        # verificar create
        manager_obj = self.env['product_autoload.manager']
        manager_obj.run(send_mail=False)

        manager_obj.update_categories()
