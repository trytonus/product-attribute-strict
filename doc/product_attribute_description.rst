Product Attribute Description
==============================

This module is used for adding attributes to products. 
This documentation describes how to add attributes to 
variants and show combination of products on a single product template.


* `Introduction`_
* `Creating a New Product`_
* `Variants`_
* `Creating new variants`_
* `Product Attributes`_
* `Attribute Sets`_
* `Attribute Creation`_

.. _Introduction:

Introduction
+++++++++++++

Tryton uses two models for managing products:

* Product Template
* Variants

A product template is a logical grouping of closely related products. An
example would be a phone and it's different features like brand, capacity
and colour would be variants. The basic idea is that a template cannot be
purchased, manufactured or sold, only it's variant can be. On the other hand,
a product template is advertized and not it's variant.

.. _Creating a new product:

Creating a New Product
+++++++++++++++++++++++

To create new product, go to ``Product`` >> ``Products``. Click on new icon
to create new record.

.. figure:: images/19.png

The following fields are present on the product template:

==============  ================================================================
  Name                                 Description
==============  ================================================================
Name            Name of product
Type            The value can be Services, Goods and Assets
Category        Where product belongs to.
Cost Price      This can be fixed or average. This tells how cost price should
                be updated. THe fixed price products ahve unchanged prices and
                average price depicts the average cost of all items in stock.
Default UOM     Default UOM for this product.
Active          Used to disable a product.
Consumable      Used to make product consumable.
Set             The product attributes can be added from here.
Code            Specific Code given to product.
==============  ================================================================

.. _Variants:

Variants
+++++++++

A product variant is the Stock Keeping Unit (SKU) for the product template.
While templates are virtual grouping of related products, the variants are
real world products. Generally there are minor varieties in the templates.
As a result, there are different SKUs present.

For example, in the phone category, the following would be the variants:

=======  ======  =========
Variant   Color   Capacity
=======  ======  =========
Code 1    Black   8 GB
Code 2    Black  16 GB
Code 3    White   8 GB
Code 4    White  16 GB
=======  ======  =========

The different characteristics which make up variations are known as Attributes.

.. _Creating new variants:

Creating Variants
+++++++++++++++++

Go to ``Product``>> ``Products`` >> ``Variants``, and click on new icon
to create a new record.

.. figure:: images/20.png

The variants window has the following fields:

=======================  ====================================================
 Name                                     Description
=======================  ====================================================
Product Template          The template of which the product is a variation of.
Code                      A unique code for the product.
Active                    The product can be disabled with this.
Attributes                Attributes of the product chosen.
=======================  ====================================================

.. _Product Attributes:

Product Attributes
+++++++++++++++++++

The attributes are the collective characteristics of proudct variants. For
example, in case of a phone, its attributes will be capacity, brand, color etc.

.. _Attribute sets:

Attribute Sets
+++++++++++++++

It is a collection of attributes. These are the collective characteristics of
variants. In case of a phone, its attributes will be brand, color, capacity etc.

.. _Attribute creation:

Creation of Attributes
++++++++++++++++++++++

.. note::

    We will use the same example of variants of a smartphone for illustration
    purposes.

1. Click on ``Product``>> ``Attibute Sets`` to create a new attribute.

.. figure:: images/1.png

2. Click on ``Create a new record``.

.. figure:: images/2.png

3. Add Name of the attribute. For illustrative purposes, we will go with
   `Phone`.
   
   Click on `Create a new record` in front of attributes.

.. figure:: images/3.png

4. Click on ``New`` to create a new record.

.. figure:: images/4.png

5. In the Name field, add Colour. From the drop down menu, click on drop-down
   and choose ``Selection``.

.. figure:: images/5.png

6. Click ``Add a new record`` next to selection.

.. figure:: images/6.png

7. In the attribute name field, add `Black` and click `Ok`.

.. figure:: images/7.png

Follow same steps to add other colors. Once done, click `Ok`. You will
be able to see attribute added. 

Repeat the same steps for adding Brand and Capacity. 

.. figure:: images/8.png

Click on ``Save this record``. 

8. Double click on `Product` tab and click on ``Create a new record``.

.. figure:: images/9.png

9. Let us now see how the attribute sets we created work. In the window that
   opens, add details of products and click on ``Search a record`` in the
   `Sets` tab. 

.. figure:: images/10.png

You can see the attribute set we created by the name `Phone`. Select and hit
Ok.

.. figure:: images/11.png

10. Click on `Create a new record` next to Attribute.

.. figure:: images/12.png

11. In the window that opens, click on `Search a new record`.

.. figure:: images/13.png

12. You can now see the attributes we defined. Select any one and hit OK.

.. figure:: images/14.png

13. In Value Selection field, click on ``Search a new record``.

.. figure:: images/15.png

14. All the enlisted colours can be seen. Select any one and click Ok.

.. figure:: images/16.png

Repeat the above steps for specifying the Brand and Capacity too. Once done,
save your records.

15. If you Switch views, you can see the specifications you selected.

.. figure:: images/17.png

.. figure:: images/18.png






 


