# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)


class CommonMapper(object):
    @staticmethod
    def check_string(field, value):
        try:
            value.decode('utf-8')
        except UnicodeError as ex:
            _logger.error('%s Value: "%s": %s', field, value, ex.message)
        return value


IM_CODE = 0
IM_NAME = 1
IM_ORIGIN = 2
IM_SECTION_CODE = 3
IM_FAMILY_CODE = 4
IM_LEN = 5


class ItemMapper(CommonMapper):
    def __init__(self, line, image_path=False, vendor=False,
                 supplierinfo=False):
        if len(line) != IM_LEN:
            raise Exception('item.csv len is %d must be %d', len(line),
                            IM_LEN)

        self._code = False
        self._name = False
        self._origin = False
        self._section_code = False
        self._family_code = False

        self.code = line[IM_CODE]
        self.name = line[IM_NAME]
        self.origin = line[IM_ORIGIN]
        self.section_code = line[IM_SECTION_CODE]
        self.family_code = line[IM_FAMILY_CODE]

    def execute(self, env):
        """
         se supone que esto no actualiza los datos, porque se borran antes de
         que se procesen asi que siempre hacemos create
        """
        try:
            section_obj = env['product_autoload.item']
            section_obj.create(self.values())
            _logger.info('Creating item %s', self.name)
        except Exception as ex:
            _logger.error(ex.message)

    def values(self):
        return {'name': self.name,
                'item_code': self.code,
                'section_code': self.section_code,
                'family_code': self.family_code}

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = self.check_string('Item Code', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.check_string('Item Name', value)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = self.check_string('Item Origin', value)

    @property
    def section_code(self):
        return self._section_code

    @section_code.setter
    def section_code(self, value):
        self._section_code = self.check_string('Item Section Code', value)

    @property
    def family_code(self):
        return self._family_code

    @family_code.setter
    def family_code(self, value):
        self._family_code = self.check_string('Item Family Code', value)


FM_CODE = 0
FM_NAME = 1
FM_LEN = 2


class FamilyMapper(CommonMapper):
    def __init__(self, line, image_path=False, vendor=False,
                 supplierinfo=False):
        if len(line) != FM_LEN:
            raise Exception('family.csv len is %d must be %d', len(line),
                            FM_LEN)

        self._code = False
        self._name = False

        self.code = line[FM_CODE]
        self.name = line[FM_NAME]

    def execute(self, env):
        """
         se supone que esto no actualiza los datos, porque se borran antes de
         que se procesen asi que siempre hacemos create
        """
        try:
            section_obj = env['product_autoload.family']
            section_obj.create(self.values())
            _logger.info('Creating family %s', self.name)
        except Exception as ex:
            _logger.error(ex.message)

    def values(self):
        return {'family_code': self.code,
                'name': self.name}

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = self.check_string('Family Code', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.check_string('Family Name', value)


SM_CODE = 0
SM_NAME = 1
SM_LEN = 2


class SectionMapper(CommonMapper):
    def __init__(self, line, image_path=False, vendor=False,
                 supplierinfo=False):
        if len(line) != SM_LEN:
            raise Exception('section.csv len is %d must be %d', len(line),
                            SM_LEN)

        self._code = False
        self._name = False

        self.code = line[SM_CODE]
        self.name = line[SM_NAME]

    def execute(self, env):
        """
         se supone que esto no actualiza los datos, porque se borran antes de
         que se procesen asi que siempre hacemos create
        """
        try:
            section_obj = env['product_autoload.section']
            section_obj.create(self.values())
            _logger.info('Creating section %s', self.name)
        except Exception as ex:
            _logger.error(ex.message)

    def values(self):
        return {
            'section_code': self.code,
            'name': self.name}

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = self.check_string('Section Code', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.check_string('Section Name', value)


MAP_DEFAULT_CODE = 0
MAP_NAME = 1
MAP_DESCRIPTION_SALE = 2
MAP_BARCODE = 3
MAP_LIST_PRICE = 4
MAP_STANDARD_PRICE = 5
MAP_WEIGHT = 6
MAP_VOLUME = 7
MAP_IMAGE_NAME = 8
MAP_WARRANTY = 9
MAP_IVA = 10
MAP_ITEM_CODE = 11
MAP_WRITE_DATE = 12
MAP_LEN = 13


class ProductMapper(CommonMapper):
    def __init__(self, line, image_path=False, vendor=False,
                 supplierinfo=False):
        if len(line) != MAP_LEN:
            raise Exception('data.csv len is %d must be %d', len(line),
                            MAP_LEN)
        self._supplierinfo_obj = supplierinfo
        self._vendor = vendor
        self._image_path = image_path
        self._default_code = False
        self._name = False
        self._description_sale = False
        self._barcode = False
        self._list_price = False
        self._standard_price = False
        self._weight = False
        self._volume = False
        self._image_name = False
        self._image = False
        self._warranty = False
        self._iva = False
        self._item_code = False
        self._write_date = False

        self.default_code = line[MAP_DEFAULT_CODE]
        self.name = line[MAP_NAME]
        self.description_sale = line[MAP_DESCRIPTION_SALE]
        self.barcode = line[MAP_BARCODE]
        self.list_price = line[MAP_LIST_PRICE]
        self.standard_price = line[MAP_STANDARD_PRICE]
        self.weight = line[MAP_WEIGHT]
        self.volume = line[MAP_VOLUME]
        self.image_name = line[MAP_IMAGE_NAME]
        self.warranty = line[MAP_WARRANTY]
        self.item_code = line[MAP_ITEM_CODE]
        self.iva = line[MAP_IVA]
        self.write_date = line[MAP_WRITE_DATE]

    def values(self, create=False):
        ret = {'default_code': self.default_code}

        if self.name:
            ret['name'] = self.name

        if self._description_sale:
            ret['description_sale'] = self.description_sale

        if self.barcode:
            ret['barcode'] = self.barcode

        if self.list_price:
            ret['list_price'] = self.list_price

        if self.standard_price:
            ret['standard_price'] = self.standard_price

        if self.weight:
            ret['weight'] = self.weight

        if self.volume:
            ret['volume'] = self.volume

        if self.warranty:
            ret['warranty'] = self.warranty

        if self.write_date:
            ret['write_date'] = self.write_date

        if self._image:
            ret['image'] = self._image

        if self.item_code:
            ret['item_code'] = self.item_code

        supplierinfo = {
            'name': self._vendor.id,
            'min_qty': 1.0,
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

    def execute(self, env):
        """
         si encuentra el producto en el modelo lo actualiza si no lo
         encuentra lo crea

        :param product_model: objeto product.product
        :return:
        """
        product_obj = env['product.product']
        prod = product_obj.search([('default_code', '=', self.default_code)])
        if prod:
            try:
                prod.write(self.values())
                _logger.info('Updating product %s', self.default_code)
            except Exception as ex:
                _logger.error(ex.message)
        else:
            try:
                product_obj.create(self.values(create=True))
                _logger.info('Creating product %s', self.default_code)
            except Exception as ex:
                _logger.error(ex.message)

    @staticmethod
    def check_numeric(field, value):
        try:
            ret = int(value)
        except ValueError as ex:
            _logger.error('%s Value: "%s": %s', field, value, ex.message)
        return value

    @staticmethod
    def check_currency(field, value):
        try:
            ret = float(value)
            return ret
        except ValueError as ex:
            _logger.error('%s Value: "%s": %s', field, value, ex.message)
        return False

    @staticmethod
    def check_float(field, value):
        try:
            ret = float(value)
            return ret
        except ValueError as ex:
            _logger.error('%s Value "%s": %s', field, value, ex.message)
        return False

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
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value):
        if value:
            self._barcode = self.check_numeric('barcode', value)

    @property
    def list_price(self):
        return self._list_price

    @list_price.setter
    def list_price(self, value):
        if value:
            self._list_price = self.check_currency('list_price', value)

    @property
    def standard_price(self):
        return self._standard_price

    @standard_price.setter
    def standard_price(self, value):
        if value:
            self._standard_price = self.check_currency('standard_price', value)

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
                logging.error('%s %s', ex.filename, ex.strerror)

    @property
    def iva(self):
        return self._iva

    @iva.setter
    def iva(self, value):
        if value:
            self._iva = self.check_float('iva', value)

            # agregar el iva
            #        taxes_id
            #        supplier_taxes_id

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
