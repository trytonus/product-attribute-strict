# -*- coding: utf-8 -*-
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
