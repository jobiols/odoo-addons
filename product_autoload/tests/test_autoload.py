# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from __future__ import division

from openerp.tests.common import TransactionCase
from ..models.mappers import ProductMapper, MAP_NAME, MAP_UPV, \
    MAP_STANDARD_PRICE, MAP_WEIGHT

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
#   oe -Q product_autoload -c iomaq -d iomaq_test
#
#

import os


class TestBusiness(TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """

    def setUp(self):
        """ Este setup corre antes de cada método ---------------------------00
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

        # definimos una linea del archivo para probar
        self.line = [
            '123456',  # Código del producto
            'nombre-producto',  # Nombre del producto
            'Descripción del producto',  # Descripción del producto
            '500.22',  # Precio de costo
            '100',  # UPV Agrupacion mayorista
            '200.50',  # Peso bruto en kg
            '125.85',  # Volumen m3
            '100',  # Bulto Mayorista
            '5',  # Bulto Minorista
            '102.7811.jpg',  # Nombre de la imagen
            '60',  # Garantia (meses)
            '15.5',  # IVA %
            '133',  # idRubro
            '2018-25-01 13:10:55']  # Timestamp actualización

        self.manager_obj = self.env['product_autoload.manager']
        self.prod_obj = self.env['product.template']

    def test_01_product_mapper(self):
        """ Chequear creacion de ProductMapper ------------------------------01
        """

        # creamos un dict con los valores pasados por el prod
        val = {
            'default_code': self.line[0],
            'name': self.line[1],
            'description_sale': self.line[2],
            'bulonfer_cost': float(self.line[3]) / float(self.line[4]),
            'upv': float(self.line[4]),
            'weight': float(self.line[5]),
            'volume': float(self.line[6]),
            'wholesaler_bulk': float(self.line[7]),
            'retail_bulk': float(self.line[8]),
            '_image_name': self.line[9],
            'warranty': float(self.line[10]),
            'iva': float(self.line[11]),
            'item_code': self.line[12],
            'write_date': self.line[13]
        }

        # cargamos la linea en el mapper
        prod = ProductMapper(self.line, self._data_path, self._vendor,
                             self._supinfo)

        # chequeamos que cada propiedad este correcta
        self.assertEqual(prod.default_code, val['default_code'])
        self.assertEqual(prod.name, val['name'])
        self.assertEqual(prod.description_sale, val['description_sale'])
        self.assertEqual(prod.bulonfer_cost, val['bulonfer_cost'])
        self.assertEqual(prod.upv, val['upv'])
        self.assertEqual(prod.weight, val['weight'])
        self.assertEqual(prod.volume, val['volume'])
        self.assertEqual(prod.wholesaler_bulk, val['wholesaler_bulk'])
        self.assertEqual(prod.retail_bulk, val['retail_bulk'])
        self.assertEqual(prod.warranty, val['warranty'])
        self.assertEqual(prod.iva, val['iva'])
        self.assertEqual(prod.item_code, val['item_code'])
        self.assertEqual(prod.write_date, val['write_date'])

        # verificamos que los datos sean correctos
        val = prod.values()
        for item in val:
            self.assertEqual(prod.values()[item], val[item])

        # verificar ademas los default values
        self.assertEqual(val['type'], 'product')
        self.assertEqual(val['invoice_policy'], 'order')
        self.assertEqual(val['purchase_method'], 'purchase')

    def test_02_(self):
        """ string no unicode -----------------------------------------------02
        """
        line = self.line
        line[MAP_NAME] = b'\x00\xFF\x00\xFF'  # string no utf-8
        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_03_(self):
        """ numero es un string ---------------------------------------------03
        """
        line = self.line
        line[MAP_UPV] = 'HHH'  # debe ser numero y es string
        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_04_(self):
        """ currency es un string -------------------------------------------04
        """
        line = self.line
        line[MAP_STANDARD_PRICE] = 'HHH'  # debe ser currency y es string
        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_05_(self):
        """ float es un string ----------------------------------------------05
        """
        line = self.line
        line[MAP_WEIGHT] = 'HHH'  # debe ser numero y es string
        with self.assertRaises(Exception):
            prod = ProductMapper(line, self._data_path, self._vendor,
                                 self._supinfo)

    def test_06_update(self):
        """ Chequear que NO replique registros viejos------------------------06
        """
        # fecha de los registros 2018-01-26 16:13:21
        # con esta fecha no deberia replicar nada
        self.env['ir.config_parameter'].set_param(
            'last_replication', '2018-02-26 16:13:21')
        self.env['ir.config_parameter'].set_param(
            'import_only_new', True)

        self.manager_obj.run()
        prod = self.prod_obj.search([('default_code', '=', '102.AF')])
        self.assertFalse(prod)
        prod = self.prod_obj.search([('default_code', '=', '106.32')])
        self.assertFalse(prod)

    def test_07_update_product(self):
        """ Chequear que SI replique registros nuevos------------------------07
        """
        # fecha de los registros 2018-01-26 16:13:21
        # con esta fecha si deberia replicar
        self.env['ir.config_parameter'].set_param(
            'last_replication', '2018-01-01 16:13:21')
        self.env['ir.config_parameter'].set_param(
            'import_only_new', True)

        self.manager_obj.run()
        prod = self.prod_obj.search([('default_code', '=', '102.AF')])
        self.assertTrue(prod)
        self.assertTrue(prod.invalidate_category)
        prod = self.prod_obj.search([('default_code', '=', '106.32')])
        self.assertTrue(prod)
        self.assertTrue(prod.invalidate_category)

    def test_08_update_product(self):
        """ Chequear que SI replique si fuerzo la replicacion----------------08
        """
        # fecha de los registros 2018-01-26 16:13:21
        # con esta fecha no deberia replicar nada
        self.env['ir.config_parameter'].set_param(
            'last_replication', '2018-02-26 16:13:21')
        # pero aca lo estoy forzando a que replique
        self.env['ir.config_parameter'].set_param(
            'import_only_new', False)

        self.manager_obj.run()
        prod = self.prod_obj.search([('default_code', '=', '102.AF')])
        self.assertTrue(prod)
        prod = self.prod_obj.search([('default_code', '=', '106.32')])
        self.assertTrue(prod)

    def test_09_categories(self):
        """ Actualizacion de categorias y precios de lista ------------------09
        """
        prod_obj = self.env['product.template']

        self.manager_obj.run()
        prod = prod_obj.search([('default_code', '=', '102.B.12')])
        self.assertEqual(prod.bulonfer_cost, 2.2372)
        prod = prod_obj.search([('default_code', '=', '106.32')])
        self.assertEqual(prod.bulonfer_cost, 15.0620)

        self.manager_obj.update_categories()

        # verificar creacion de categorias
        categ_obj = self.env['product.category']
        categs = categ_obj.search([('name', '=', 'Ferretería'),
                                   ('parent_id', '=', False)])
        self.assertEqual(len(categs), 1)

        # verificar precios de lista
        prod = prod_obj.search([('default_code', '=', '102.B.12')])
        self.assertAlmostEqual(prod.list_price, 2.2372 * 1.5, places=2)
        prod = prod_obj.search([('default_code', '=', '106.32')])
        self.assertAlmostEqual(prod.list_price, 15.0620 * 1.5, places=2)

    def test_10_cambia_margen(self):
        """ Testear cambio de margen de ganancia-----------------------------10
        """

        self.manager_obj.run()
        self.manager_obj.update_categories()

        prod = self.prod_obj.search([('default_code', '=', '106.24')])
        self.assertAlmostEqual(prod.bulonfer_cost, 150.62)
        self.assertAlmostEqual(prod.bulonfer_cost * 1.5, prod.list_price,
                               places=2)

        self.manager_obj.run(item='item_changed.csv')
        self.manager_obj.update_categories()

        prod = self.prod_obj.search([('default_code', '=', '106.24')])
        self.assertAlmostEqual(prod.bulonfer_cost * 1.6, prod.list_price,
                               places=2)

