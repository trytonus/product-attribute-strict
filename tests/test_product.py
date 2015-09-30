# -*- coding: utf-8 -*-
import unittest
import sys
import os
from decimal import Decimal
from datetime import datetime
from datetime import date
from datetime import time

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.transaction import Transaction
from trytond.exceptions import UserError

DIR = os.path.abspath(os.path.normpath(os.path.join(
    __file__, '..', '..', '..', '..', '..', 'trytond'
)))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))


class TestProduct(unittest.TestCase):
    '''
    Test Product
    '''

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        trytond.tests.test_tryton.install_module('product_attribute_strict')

        self.Template = POOL.get('product.template')
        self.Product = POOL.get('product.product')
        self.Attribute = POOL.get('product.attribute')
        self.AttributeSet = POOL.get('product.attribute.set')
        self.SelectionOption = POOL.get('product.attribute.selection_option')
        self.Uom = POOL.get('product.uom')

    def _create_product_template(self, attribute_set=None):
        """
        Create default product template
        """
        return self.Template.create([{
            'name': 'Test Template 1',
            'default_uom': self.Uom.search([('name', '=', 'Unit')])[0],
            'list_price': Decimal('10'),
            'cost_price': Decimal('5'),
            'attribute_set': attribute_set,
        }])[0]

    def test0010_add_product_attributes(self):
        """
        Check if attributes can be added to product
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):

            # Create Attributes

            # Char attribute
            char_attr, = self.Attribute.create([{
                'name': 'Test Char',
            }])

            self.assertEqual(char_attr.type_, 'char')

            # Float attribute
            float_attr, = self.Attribute.create([{
                'type_': 'float',
                'display_name': 'Float',
                'name': 'Test Float',
            }])

            # Numeric Attribute
            numeric_attr, = self.Attribute.create([{
                'type_': 'numeric',
                'display_name': 'Numeric',
                'name': 'Test Numeric',
            }])

            # Datetime Attribute
            datetime_attr, = self.Attribute.create([{
                'type_': 'datetime',
                'display_name': 'Datetime',
                'name': 'Test Datetime',
            }])

            # Date Attribute
            date_attr, = self.Attribute.create([{
                'type_': 'date',
                'display_name': 'Date',
                'name': 'Test Date',
            }])

            # Selection Attribute
            selection_attr, = self.Attribute.create([{
                'type_': 'selection',
                'display_name': 'Selection',
                'name': 'Test Selection',
                'selection': [
                    ('create', [{
                        'name': 'option1'
                    }, {
                        'name': 'option2'
                    }])
                ]
            }])

            # Rec name for attribute without display name
            self.assertEqual(char_attr.rec_name, char_attr.name)

            # Rec name for attribute with both name and display name
            self.assertEqual(float_attr.rec_name, float_attr.display_name)

            # Create Attribute sets
            attribute_set1, = self.AttributeSet.create([{
                'name': 'Test attribute set 1',
                'attributes': [('add', [
                    char_attr.id, selection_attr.id, datetime_attr.id,
                    date_attr.id
                ])]
            }])

            attribute_set2, = self.AttributeSet.create([{
                'name': 'Test attribute set 2',
                'attributes': [('add', [numeric_attr.id, float_attr.id])]
            }])

            # Create selection option for selection attribute
            option1, = self.SelectionOption.create([{
                'name': 'Test Option 1',
                'attribute': selection_attr
            }])

            template = self._create_product_template(attribute_set1)

            # Create product with attributes defined for attribute set 1
            # Attributes to be added must be part of attribute set defined
            # for template
            prod1, = self.Product.create([{
                'template': template.id,
                'attributes': [
                    ('create', [{
                        'attribute': char_attr.id,
                        'value_char': 'Test Char Value',
                    }, {
                        'attribute': selection_attr.id,
                        'value_selection': option1.id,
                    }, {
                        'attribute': datetime_attr.id,
                        'value_datetime': datetime.now(),
                    }, {
                        'attribute': date_attr.id,
                        'value_date': date.today(),
                    }])
                ]
            }])

            # Test the value field
            self.assertEqual(
                prod1.attributes[0].value,
                prod1.attributes[0].value_char
            )
            self.assertEqual(
                prod1.attributes[1].value,
                prod1.attributes[1].value_selection.name
            )
            self.assertEqual(
                prod1.attributes[2].value,
                prod1.attributes[2].value_datetime.strftime("%Y-%m-%d %H:%M:%S")
            )
            self.assertEqual(
                prod1.attributes[3].value,
                datetime.combine(
                    prod1.attributes[3].value_date,
                    time()
                ).strftime("%Y-%m-%d")
            )

            #  Try creating product with attributes defined for attribute
            #  set 2 ( not part of attribute set defined for template), and
            #  error will be raised
            with self.assertRaises(UserError):
                self.Product.create([{
                    'template': template.id,
                    'attributes': [
                        ('create', [{
                            'attribute': numeric_attr.id,
                            'value_numeric': Decimal('10'),
                        }])
                    ]
                }])
                self.Product.create([{
                    'template': template.id,
                    'attributes': [
                        ('create', [{
                            'attribute': float_attr.id,
                            'value_float': 1.23,
                        }])
                    ]
                }])

            # check on_change value for attribute type
            prod_attribute = prod1.attributes[0]
            prod_attribute.on_change_attribute()

            self.assertEqual(
                prod_attribute.attribute_type, prod_attribute.attribute.type_
            )

            # check value for attribute set by changing product
            prod_attribute.on_change_product()

            self.assertEqual(
                prod_attribute.attribute_set,
                prod_attribute.product.template.attribute_set
            )


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestProduct)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
