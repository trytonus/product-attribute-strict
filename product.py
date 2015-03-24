# -*- coding: utf-8 -*-
"""
    product_attribute_strict.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__metaclass__ = PoolMeta
__all__ = [
    'ProductAttributeSet', 'ProductAttributeSelectionOption',
    'ProductAttribute', 'ProductAttributeAttributeSet',
    'Template', 'ProductProductAttribute', 'Product',
]

ATTRIBUTE_TYPES = [
    ('boolean', 'Boolean'),
    ('integer', 'Integer'),
    ('char', 'Char'),
    ('float', 'Float'),
    ('numeric', 'Numeric'),
    ('date', 'Date'),
    ('datetime', 'DateTime'),
    ('selection', 'Selection'),
]


class ProductAttributeSet(ModelSQL, ModelView):
    "Product Attribute Set"
    __name__ = 'product.attribute.set'

    name = fields.Char('Name', required=True, select=True, translate=True)
    attributes = fields.Many2Many(
        'product.attribute-product.attribute-set',
        'attribute_set', 'attribute', 'Attributes'
    )


class ProductAttributeSelectionOption(ModelSQL, ModelView):
    "Attribute Selection Option"

    __name__ = 'product.attribute.selection_option'

    name = fields.Char("Name", required=True, select=True, translate=True)
    attribute = fields.Many2One(
        "product.attribute", "Attribute", required=True, ondelete='CASCADE'
    )


class ProductAttribute(ModelSQL, ModelView):
    "Product Attribute"
    __name__ = 'product.attribute'

    sets = fields.Many2Many(
        'product.attribute-product.attribute-set',
        'attribute', 'attribute_set', 'Sets'
    )

    name = fields.Char('Name', required=True, select=True, translate=True)
    display_name = fields.Char('Display Name', translate=True)
    type_ = fields.Selection(
        ATTRIBUTE_TYPES, 'Type', required=True, select=True
    )

    selection = fields.One2Many(
        "product.attribute.selection_option", "attribute", "Selection",
        states={
            'invisible': ~(Eval('type_') == 'selection'),
        }
    )

    def get_rec_name(self, name):
        return self.display_name or self.name

    @staticmethod
    def default_type_():
        return 'char'


class ProductAttributeAttributeSet(ModelSQL):
    "Product Attribute - Set"
    __name__ = 'product.attribute-product.attribute-set'

    attribute = fields.Many2One(
        'product.attribute', 'Attribute',
        ondelete='CASCADE', select=True, required=True
    )
    attribute_set = fields.Many2One(
        'product.attribute.set', 'Set',
        ondelete='CASCADE', select=True, required=True
    )


class Template:
    "Template"
    __name__ = 'product.template'

    attribute_set = fields.Many2One(
        'product.attribute.set', 'Set', ondelete='RESTRICT'
    )


class ProductProductAttribute(ModelSQL, ModelView):
    "Product's Product Attribute"
    __name__ = 'product.product.attribute'

    product = fields.Many2One(
        "product.product", "Product", select=True, required=True
    )

    attribute = fields.Many2One(
        "product.attribute", "Attribute", required=True, select=True,
        domain=[('sets', '=', Eval('attribute_set'))],
        depends=['attribute_set'], ondelete='RESTRICT'
    )

    attribute_type = fields.Function(
        fields.Selection(ATTRIBUTE_TYPES, "Attribute Type"),
        'on_change_with_attribute_type'
    )

    attribute_set = fields.Function(
        fields.Many2One("product.attribute.set", "Attribute Set"),
        'on_change_with_attribute_set'
    )

    value_char = fields.Char(
        "Value Char", states={
            'required': Eval('attribute_type') == 'char',
            'invisible': ~(Eval('attribute_type') == 'char'),
        }, depends=['attribute_type']
    )
    value_numeric = fields.Numeric(
        "Value Numeric", states={
            'required': Eval('attribute_type') == 'numeric',
            'invisible': ~(Eval('attribute_type') == 'numeric'),
        }, depends=['attribute_type']
    )
    value_float = fields.Float(
        "Value Float", states={
            'required': Eval('attribute_type') == 'float',
            'invisible': ~(Eval('attribute_type') == 'float'),
        }, depends=['attribute_type']
    )

    value_selection = fields.Many2One(
        "product.attribute.selection_option", "Value Selection",
        domain=[('attribute', '=', Eval('attribute'))],
        states={
            'required': Eval('attribute_type') == 'selection',
            'invisible': ~(Eval('attribute_type') == 'selection'),
        }, depends=['attribute', 'attribute_type'],
        ondelete='RESTRICT'
    )

    value_boolean = fields.Boolean(
        "Value Boolean", states={
            'required': Eval('attribute_type') == 'boolean',
            'invisible': ~(Eval('attribute_type') == 'boolean'),
        }, depends=['attribute_type']
    )
    value_integer = fields.Integer(
        "Value Integer", states={
            'required': Eval('attribute_type') == 'integer',
            'invisible': ~(Eval('attribute_type') == 'integer'),
        }, depends=['attribute_type']
    )
    value_date = fields.Date(
        "Value Date", states={
            'required': Eval('attribute_type') == 'date',
            'invisible': ~(Eval('attribute_type') == 'date'),
        }, depends=['attribute_type']
    )
    value_datetime = fields.DateTime(
        "Value Datetime", states={
            'required': Eval('attribute_type') == 'datetime',
            'invisible': ~(Eval('attribute_type') == 'datetime'),
        }, depends=['attribute_type']
    )

    @fields.depends('attribute')
    def on_change_with_attribute_type(self, name=None):
        """
        Returns type of attribute
        """
        if self.attribute:
            return self.attribute.type_

    @fields.depends('product')
    def on_change_with_attribute_set(self, name=None):
        """
        Returns attribute set for corresponding product's template
        """
        if self.product and self.product.template.attribute_set:
            return self.product.template.attribute_set.id


class Product:
    "Product"
    __name__ = 'product.product'

    attributes = fields.One2Many(
        "product.product.attribute", "product", "Attributes",
        domain=[(
            'attribute.sets', '=',
            Eval('_parent_template', {}).get('attribute_set',
                Eval('attribute_set', -1)
            )
        )], states={
            'readonly': (
                ~Eval('attribute_set')
                & ~Eval('_parent_template', {}).get('attribute_set')
            ),
        }, depends=['attribute_set'], context={
            'attribute_set': Eval('attribute_set')
        }
    )

    attribute_set = fields.Function(
        fields.Many2One('product.attribute.set', 'Set'),
        'on_change_with_attribute_set',
    )

    @fields.depends('template')
    def on_change_with_attribute_set(self, name=None):
        if self.template and getattr(self.template, 'attribute_set', None):
            return self.template.attribute_set.id

        return Transaction().context.get('attribute_set')  # pragma: no cover
