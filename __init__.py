# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool

from product import (
    ProductAttributeSet, ProductAttributeSelectionOption, ProductAttribute,
    ProductAttributeAttributeSet, Template, ProductProductAttribute, Product
)


def register():
    Pool.register(
        ProductAttributeSet,
        ProductAttribute,
        ProductAttributeSelectionOption,
        ProductAttributeAttributeSet,
        Template,
        ProductProductAttribute,
        Product,
        module='product_attribute_strict', type_='model'
    )
