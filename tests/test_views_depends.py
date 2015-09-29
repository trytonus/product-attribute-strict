# -*- coding: utf-8 -*-
"""
    tests/test_views_depends.py

    :copyright: (C) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest
import sys
import os

import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase

DIR = os.path.abspath(os.path.normpath(os.path.join(
    __file__, '..', '..', '..', '..', '..', 'trytond'
)))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))


class TestViewsDepends(ModuleTestCase):
    '''
    Test views and depends
    '''

    module = 'product_attribute_strict'


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestViewsDepends)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
