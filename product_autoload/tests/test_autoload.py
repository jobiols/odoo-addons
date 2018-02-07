# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division

from openerp.tests.common import TransactionCase
from ..models.mappers import ProductMapper, SectionMapper, FamilyMapper, \
    ItemMapper

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
        self._vendor = self.env['res.partner'].search(
            [('name', 'like', 'Bulonfer')])
        self._supinfo = self.env['product.supplierinfo']

    def test_02_product_mapper(self):
        """ Chequear creacion de ProductMapper ------------------------------02
        """
        line = [
            '123456',
            'nombre-producto',
            'Descripción del producto',
            '7750082001169',
            '1000.52',
            '500.22',
            '200.50',
            '125.85',
            '601.AA.3157.jpg',
            '60',
            '21',
            '001',
            '2018-25-01 13:10:55']

        prod = ProductMapper(line, self._data_path, self._vendor,
                             self._supinfo)
        self.assertEqual(prod.default_code, '123456')
        self.assertEqual(prod.name, 'nombre-producto')
        self.assertEqual(prod.description_sale, 'Descripción del producto')
        self.assertEqual(prod.barcode, '7750082001169', )
        self.assertEqual(prod.list_price, 1000.52)
        self.assertEqual(prod.standard_price, 500.22)
        self.assertEqual(prod.weight, 200.50)
        self.assertEqual(prod.volume, 125.85)
        self.assertEqual(prod.warranty, 60)
        self.assertEqual(prod.iva, 21)
        self.assertEqual(prod.item_code, '001')
        self.assertEqual(prod.write_date, '2018-25-01 13:10:55')

        val = {
            'warranty': 60.0,
            'barcode': '7750082001169',
            'list_price': 1000.52,
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

    def test_04_update_product(self):
        """ Chequear update de producto -------------------------------------04
        """
        # verificar createm
        product_obj = self.env['product.product']
        product_obj.auto_load(self._data_path)

        #        prod_obj = self.env['product.product']
        #        prod = prod_obj.search([('default_code', '=', '601.AA.315/7')])
        #        self.assertEqual(len(prod), 1)
        #        self.assertEqual(prod.item_code, '001')

        #        prod = prod_obj.search([('default_code', '=', '601.HV.8800B')])
        #        self.assertEqual(len(prod), 1)
        #        self.assertEqual(prod.item_code, '001')

        #        prod = prod_obj.search([('default_code', '=', '601.I.10250')])
        #        self.assertEqual(len(prod), 1)
        #        self.assertEqual(prod.item_code, '003')

        # verificar update

    #        product_obj.auto_load(self._data_path)

    def test_05_section_mapper(self):
        """ Testear seccion mapper ------------------------------------------05
        """
        line = ['1',
                'Buloneria']
        section = SectionMapper(line)
        self.assertEqual(section.code, '1')
        self.assertEqual(section.name, 'Buloneria')

    def test_06_family_mapper(self):
        """ Testear Family mapper -------------------------------------------06
        """
        line = ['3C',
                'MANGERAS TRICOLOR']
        family = FamilyMapper(line)
        self.assertEqual(family.code, '3C')
        self.assertEqual(family.name, 'MANGERAS TRICOLOR')

    def test_07_item_mapper(self):
        """ Testear Item mapper ---------------------------------------------07
        """
        line = ['001',
                'BULON PULIDO FIXO',
                'Importado',
                '1',
                'BG2']
        item = ItemMapper(line)
        self.assertEqual(item.code, '001')
        self.assertEqual(item.name, 'BULON PULIDO FIXO')
        self.assertEqual(item.origin, 'Importado')
        self.assertEqual(item.section_code, '1')
        self.assertEqual(item.family_code, 'BG2')

    def test_08_load_section(self):
        """ Testear load section---------------------------------------------08
        """
        product_obj = self.env['product.product']
        product_obj.process_file(self._data_path, 'section.csv', SectionMapper)

    def test_09_load_family(self):
        """ Testear load section---------------------------------------------09
        """
        product_obj = self.env['product.product']
        product_obj.process_file(self._data_path, 'family.csv', FamilyMapper)

    def test_10_load_item(self):
        """ Testear load section---------------------------------------------10
        """
        product_obj = self.env['product.product']
        product_obj.process_file(self._data_path, 'item.csv', ItemMapper)

    def test_11_item_unlink(self):
        """ Testear que el unlink borra todo --------------------------------11
        """
        product_obj = self.env['product.product']
        # cargar productos
        product_obj.auto_load(self._data_path)
        # cargar categorias
        product_obj.category_load(self._data_path)

        item_obj = self.env['product_autoload.item']
        item_obj.unlink_data()

        items = self.env['product_autoload.item'].search([])
        self.assertEqual(len(items), 0)
        sections = self.env['product_autoload.section'].search([])
        self.assertEqual(len(sections), 0)
        families = self.env['product_autoload.family'].search([])
        self.assertEqual(len(families), 0)

    def test_12_item_unlink(self):
        """ Testear que el unlink borra todo --------------------------------12
        """
        product_obj = self.env['product.product']
        # cargar productos
        product_obj.auto_load(self._data_path)
        # cargar categorias
        product_obj.category_load(self._data_path)

    def test_13_check_all(self):
        """ cargar todo dos veces para asegurar multiples cargas-------------13
        """
        product_obj = self.env['product.product']
        # cargar productos
        product_obj.auto_load(self._data_path)
        product_obj.auto_load(self._data_path)
