# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)


class CommonMapper(object):
    @staticmethod
    def check_string(field, value):
        try:
            value.decode('utf-8')
        except:
            raise Exception(
                'Unicode Encode Error in field {}, '
                'The codification must be utf-8'.format(field))
        return value

    @staticmethod
    def check_numeric(field, value):
        try:
            ret = int(value)
        except ValueError as ex:
            _logger.error(
                '{} Value: "{}": {}'.format(field, value, ex.message))
        return ret


MAP_DEFAULT_CODE = 0
MAP_NAME = 1
MAP_DESCRIPTION_SALE = 2
MAP_STANDARD_PRICE = 3
MAP_UPV = 4
MAP_WEIGHT = 5
MAP_VOLUME = 6
MAP_WHOLESALER_BULK = 7
MAP_RETAIL_BULK = 8
MAP_IMAGE_NAME = 9
MAP_WARRANTY = 10
MAP_IVA = 11
MAP_ITEM_CODE = 12
MAP_WRITE_DATE = 13
MAP_LEN = 14


class ProductMapper(CommonMapper):
    def __init__(self, line, image_path=False, vendor=False,
                 supplierinfo=False):

        if len(line) != MAP_LEN:
            raise Exception('data.csv len is {} '
                            'must be {}'.format(len(line), MAP_LEN))
        self._supplierinfo_obj = supplierinfo
        self._vendor = vendor
        self._image_path = image_path
        self._image = False

        self._default_code = False
        self._name = False
        self._description_sale = False
        self._standard_price = False
        self._upv = False
        self._weight = False
        self._volume = False
        self._wholesaler_bulk = False
        self._retail_bulk = False
        self._image_name = False
        self._warranty = False
        self._iva = False
        self._item_code = False
        self._write_date = False

        self.default_code = line[MAP_DEFAULT_CODE]
        self.name = line[MAP_NAME]
        self.description_sale = line[MAP_DESCRIPTION_SALE]
        self.standard_price = line[MAP_STANDARD_PRICE]
        self.upv = line[MAP_UPV]
        self.weight = line[MAP_WEIGHT]
        self.volume = line[MAP_VOLUME]
        self.wholesaler_bulk = line[MAP_WHOLESALER_BULK]
        self.retail_bulk = line[MAP_RETAIL_BULK]
        self.image_name = line[MAP_IMAGE_NAME]
        self.warranty = line[MAP_WARRANTY]
        self.iva = line[MAP_IVA]
        self.item_code = line[MAP_ITEM_CODE]
        self.write_date = line[MAP_WRITE_DATE]

    def values(self, create=False):
        ret = {'default_code': self.default_code}

        if self.name:
            ret['name'] = self.name

        if self._description_sale:
            ret['description_sale'] = self.description_sale

        if self.standard_price:
            ret['standard_price'] = self.standard_price

        if self.upv:
            ret['upv'] = self.upv

        if self.weight:
            ret['weight'] = self.weight

        if self.volume:
            ret['volume'] = self.volume

        if self.wholesaler_bulk:
            ret['wholesaler_bulk'] = self.wholesaler_bulk

        if self.retail_bulk:
            ret['retail_bulk'] = self.retail_bulk

        if self.warranty:
            ret['warranty'] = self.warranty

        if self.write_date:
            ret['write_date'] = self.write_date

        if self.item_code:
            ret['item_code'] = self.item_code

        if self._image:
            ret['image'] = self._image

        supplierinfo = {
            'name': self._vendor.id,
            'min_qty': self.wholesaler_bulk,
            'price': self.standard_price,
            'product_code': self.default_code
        }
        if create:
            ret['seller_ids'] = [(0, 0, supplierinfo)]
        else:
            rec = self._supplierinfo_obj.search(
                [('name', '=', self._vendor.id),
                 ('product_code', '=', self.default_code)])
            if rec:
                rec.price = self.standard_price
            else:
                ret['seller_ids'] = [(0, 0, supplierinfo)]

        # agregar valores por defecto
        ret.update(self.default_values())
        return ret

    @staticmethod
    def default_values():
        return {
            'type': 'product',
            'invoice_policy': 'order',
            'purchase_method': 'purchase'
        }

    # TODO aca en lugar de poner none_categ_id hay que poner una marca para revisar la categoria
    # en el siguiente paso de la replicacion
    def execute(self, env, none_categ_id):
        """ Este es el corazon del proceso de replicacion, si encuentra el
            producto en el modelo lo actualiza si no lo encuentra lo crea.
        """
        product_obj = env['product.template']
        prod = product_obj.search([('default_code', '=', self.default_code)])
        if prod:
            prod.write(self.values())
            _logger.info('Updating product {}'.format(self.default_code))
        else:
            prod = product_obj.create(self.values(create=True))
            _logger.info('Creating product {}'.format(self.default_code))

        tax_obj = env['account.tax']

        # actualiza IVA ventas
        tax_sale = tax_obj.search([('amount', '=', self.iva),
                                   ('tax_group_id.tax', '=', 'vat'),
                                   ('type_tax_use', '=', 'sale')])
        if not tax_sale:
            raise Exception('Product {} needs Customer Tax {}% (IVA Sales)'
                            ' not found in Accounting'.format(
                self.default_code, self.iva))

        # si hay mas de uno me quedo con el primero
        tax = tax_sale[0].id
        prod.taxes_id = [(6, 0, [tax])]

        # actualiza iva compras
        tax_purchase = tax_obj.search([('amount', '=', self.iva),
                                       ('tax_group_id.tax', '=', 'vat'),
                                       ('type_tax_use', '=', 'purchase')])
        if not tax_purchase:
            raise Exception('Product {} needs Customer Tax {}% (IVA Purchases)'
                            ' not found in Accounting'.format(
                self.default_code, self.iva))

        # si hay mas de uno me quedo con el primero
        tax = tax_purchase[0].id
        prod.supplier_taxes_id = [(6, 0, [tax])]

        # linkear los barcodes
        prodcode_obj = env['product_autoload.productcode']
        barcode_obj = env['product.barcode']

        recs = prodcode_obj.search([('product_code', '=', prod.default_code)])
        for rec in recs:
            _logger.info('Linking barcode {}'.format(rec.barcode))
            bc = barcode_obj.search([('name', '=', rec.barcode)])
            if not bc:
                barcode_obj.create({
                    'product_id': prod.id, 'name': rec.barcode
                })
        prod.categ_id = none_categ_id

    @staticmethod
    def check_currency(field, value):
        try:
            ret = float(value)
            return ret
        except ValueError as ex:
            raise Exception(
                '{} Value: "{}": {}'.format(field, value, ex.message))

    @staticmethod
    def check_float(field, value):
        try:
            ret = float(value)
            return ret
        except ValueError as ex:
            raise Exception(
                '{} Value "{}": {}'.format(field, value, ex.message))

    def slugify(self, field, value):
        ret = self.check_string(field, value)
        ret.replace('/', '')
        return ret

    @property
    def default_code(self):
        return self._default_code

    @default_code.setter
    def default_code(self, value):
        self._default_code = self.check_string('default_code', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            self._name = self.check_string('name', value)

    @property
    def description_sale(self):
        return self._description_sale

    @description_sale.setter
    def description_sale(self, value):
        if value:
            self._description_sale = self.check_string('description_sale',
                                                       value)

    @property
    def upv(self):
        return self._upv

    @upv.setter
    def upv(self, value):
        if value:
            self._upv = self.check_numeric('upv', value)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value:
            self._weight = self.check_float('weight', value)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value:
            self._volume = self.check_float('volume', value)

    @property
    def wholesaler_bulk(self):
        return self._wholesaler_bulk

    @wholesaler_bulk.setter
    def wholesaler_bulk(self, value):
        self._wholesaler_bulk = self.check_numeric('wholesaler_bulk', value)

    @property
    def retail_bulk(self):
        return self._retail_bulk

    @retail_bulk.setter
    def retail_bulk(self, value):
        self._retail_bulk = self.check_numeric('retail_bulk', value)

    @property
    def standard_price(self):
        return self._standard_price

    @standard_price.setter
    def standard_price(self, value):
        if value:
            self._standard_price = self.check_currency('standard_price', value)

    @property
    def image_name(self):
        return self._image_name

    @image_name.setter
    def image_name(self, value):
        if value:
            self._image_name = self.slugify('image_name', value)
            # cargar la imagen
            try:
                with open(self._image_path + self._image_name,
                          'rb') as img_file:
                    self._image = img_file.read().encode('base64')
            except IOError as ex:
                logging.error('{} {}'.format(ex.filename, ex.strerror))

    @property
    def iva(self):
        return self._iva

    @iva.setter
    def iva(self, value):
        if value:
            self._iva = self.check_float('iva', value)

    @property
    def warranty(self):
        return self._warranty

    @warranty.setter
    def warranty(self, value):
        if value:
            self._warranty = self.check_float('warranty', value)

    @property
    def item_code(self):
        return self._item_code

    @item_code.setter
    def item_code(self, value):
        self._item_code = self.check_string('Item Code', value)
