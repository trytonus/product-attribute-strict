Product Attributes (Strict)
===========================

Tryton has a powerful system of attributes for products introduced by the
``product_attribute`` module. The module however uses the ``fields.Dict``
(JSON in database) field type to store attributes and this reduces the
consistency since the lack of foreign keys and constraints allow deletion,
renaming and editing of selection values even when used by products. 

**This is an experimental module trying to solve a problem in two ways.
The best solution would be chosen based on acceptable code complexity and
performance for 10000 products (the average number of SKUs Openlabs
customers have).**

Solution 1: The Constraint Solution
-----------------------------------

It should be possible to implement a validation at the level of tryton
models. This would probably involve overwriting the write method or
implementing a validation that can ensure the data is consistent.

This would certainly be a slow process and the use of `Postgres JSON
Functions <http://www.postgresql.org/docs/current/static/functions-json.html>`_
could probably speed this up. 

Implement validation on following:

1. Product Variant
```````````````````
On saving a product ensure that the attribute values are still valid
values based on the attribute and attribute set.

2. Attribute
````````````

On saving attributes of selection type, ensure that the changes do not
make any of the existing attributes invalid.

Solution 2: The RDBMS solution
------------------------------
Another possible solution is to use a database implementation 
pattern commonly known as `Entity Attribute Value (EAV) 
<https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model>`_
model to store attributes instead of the JSON field.

More implementation details
```````````````````````````

* Adds a new attribute ``type_`` called ``Strict Selection`` which allows
  possible options of the attribute selection to be created. This would be
  stored in a new model ``product.attribute.option``
* Removes the possibilty to use ``selection`` type which used JSON field
  to store the value.
* Replaces the dictionary field used to store attributes with a
  ``One2Many`` field to model ``product.product.attribute``. This would
  have a field for each type of attribute.
