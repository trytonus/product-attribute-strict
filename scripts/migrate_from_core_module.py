#! /usr/bin/env python
import os
import json
from collections import defaultdict

from trytond.config import config
config.update_etc()

from trytond.pool import Pool
from trytond.transaction import Transaction


def get_selection_json(db_selection):
    selection = [[w.strip() for w in v.split(':', 1)]
        for v in db_selection.splitlines() if v]  # noqa
    return json.loads(json.dumps(selection))


def rename_string_to_display_name():
    """Core product attribute was using string field which have been changed
    to display_name now.
    """
    cursor = Transaction().cursor
    cursor.execute(
        "ALTER TABLE product_attribute RENAME string TO display_name"
    )


def copy_selection_options():
    """
    Copy the selection field options and create options
    for the selection field.
    """
    Option = Pool().get('product.attribute.selection_option')

    cursor = Transaction().cursor
    cursor.execute(
        """
        SELECT id, selection
        FROM product_attribute
        WHERE type_='selection'
        """
    )
    # Key value map
    attribute_kv_map = defaultdict(dict)
    for row in cursor.fetchall():
        id, selection = row
        for k, v in get_selection_json(selection):
            option = Option(
                name=v, attribute=id
            )
            option.save()
            attribute_kv_map[id][k] = option.id

    print "Created selection values for %d attributes" % len(attribute_kv_map)
    return attribute_kv_map


def validate_and_copy_attributes(product, attribute_kv_map):
    """
    Validate first and copy the attributes over.
    """
    Option = Pool().get('product.attribute.selection_option')
    Attribute = Pool().get('product.attribute')
    AttrValue = Pool().get('product.product.attribute')

    print "*** Migrating Product: %s ***" % product.rec_name

    # Step 1: Get the attributes of product from database.
    #         (Could have fetched from model, but better assume the worst
    #         where the core module could have been uninstalled)
    cursor = Transaction().cursor
    cursor.execute(
        """
        SELECT attributes
        FROM product_product
        WHERE id=%s
        """, (product.id, )
    )
    attributes = cursor.fetchone()[0]

    print "Attributes: %s, (%s)" % (attributes, type(attributes))

    if attributes in (None, '{}'):
        return

    if not product.attribute_set:
        message = (
            "Product '%s' has no attribute set defined but has attributes\n"
            "defined: %s\n"
            "Options:\n"
            "(r) Remove attributes and continue\n"
            "(q) Quit, set attribute set manually and restart script"
        ) % (
            product.rec_name,
            attributes
        )
        answer = q_and_a(message, ['r', 'q'])
        if answer == 'r':
            product.attributes = []
            product.save()
            return
        else:
            raise Exception('You asked me to quit!')

    for attr_name, attr_value in json.loads(attributes).iteritems():
        # Ensure that the attribute exists
        try:
            attribute, = Attribute.search([('name', '=', attr_name)])
        except ValueError:
            message = (
                "Product %s has attribute named %s,"
                " but no such attribute exists\n"
                "Hint: Value is %s\n"
                "(c) Create a new attribute '%s'\n"
                "(q) Quit, fix it manually and restart script" % (
                    product.rec_name, attr_name, attr_value, attr_name
                )
            )
            answer = q_and_a(message, ['c', 'q'])
            if answer == 'c':
                attribute = Attribute(
                    name=attr_name,
                    type_='selection',
                    sets=[product.attribute_set],
                )
                attribute.save()
            else:
                raise Exception("You asked me to quit!")

        values = {
            'attribute': attribute,
        }

        # Ensure that the attribute exists in the attribute set
        if attribute not in product.attribute_set.attributes:
            question = (
                "Attribute '%s' is not in attribute set '%s' used by product '%s'\n"  # noqa
                "Options:\n"
                "(a) Add attribute '%s' to attribute set '%s'\n"
                "(r) Remove attribute '%s' from product '%s'\n"
                "(q) Quit and resolve yourself." % (
                    attribute.name, product.attribute_set.name, product.rec_name,  # noqa
                    attribute.name, product.attribute_set.name,
                    attribute.name, product.rec_name,
                )
            )
            answer = q_and_a(question, ['a', 'r', 'q'])
            if answer == 'a':
                product.attribute_set.attributes.append(attribute)
                product.attribute_set.save()
            elif answer == 'r':
                continue
            else:
                raise Exception('You asked me to quit!')

        # if attribute type is selection, then validate the keys that
        # they exist.
        if attribute.type_ == 'selection' and \
                attr_value not in attribute_kv_map[attribute.id]:
            question = (
                "Attribute value '%s' of attribute '%s' is not a valid selection\n"  # noqa
                "(a) Add '%s' as a valid option of attribute '%s'\n"
                "(r) Remove the attribute '%s' from product '%s'\n"
                "(c) Choose another value from valid options of '%s' (permanently)\n"  # noqa
                "(q) Quit and resolve yourself."
                % (
                    attr_value, attribute.name,
                    attr_value, attribute.name,
                    attr_value, product.rec_name,
                    attribute.name,
                )
            )
            answer = q_and_a(question, ['a', 'r', 'c', 'q'])
            if answer == 'a':
                option = Option(
                    name=attr_value, attribute=attribute
                )
                option.save()
                attribute_kv_map[attribute.id][attr_value] = option.id
            elif answer == 'r':
                continue
            elif answer == 'c':
                options = list(enumerate(
                    [opt.name for opt in attribute.selection], start=1
                ))

                question = (
                    "Select option:"
                    "\n".join("%s: %s" % option for option in options)
                )
                answer = q_and_a(question, range(1, len(options)), int)

                # map the attribute key forever to the newly chosen
                # alternative
                attribute_kv_map[attribute.id][attr_value] = answer
            else:
                raise Exception('You asked me to quit!')

        if attribute.type_ == 'selection':
            values['value_selection'] = \
                attribute_kv_map[attribute.id][attr_value]
        else:
            values['value_%s' % attribute.type_] = attr_value

        print "Saving attribute: %s" % values
        if product.attributes:
            product.attributes.append(AttrValue(**values))
        else:
            product.attributes = [AttrValue(**values)]

    product.save()


def q_and_a(question, options, cast=str):
    """
    A Q & A helper
    """
    print "*" * 80
    print "Your attention please:"
    print "*" * 80
    question += "\n\nYour Choice [%s] ?: " % (','.join(options))
    answer = None
    while answer is None:
        answer = raw_input(question)
        if cast(answer) in options:
            return cast(answer)
        else:
            answer = None


def ensure_core_module_is_installed():
    IRModule = Pool().get('ir.module.module')

    modules = IRModule.search([('name', '=', 'product_attribute')])

    if not modules:
        return True

    if modules and modules[0].state == 'uninstalled':
        return True

    answer = q_and_a(
        "The core product_attribute module is still installed.\n"
        "Hint: It is safe to uninstall as the database columns are untouched.\n"
        "Shall I uninstall the module ['y', 'n', 'q']?\n",
        ('y', 'n', 'q')
    )
    if answer == 'y':
        IRModule.uninstall(modules)
        print "Please restart this script to continue."
        return False
    else:
        raise Exception('Cannot continue when core module is installed!')


if __name__ == '__main__':
    try:
        DB_NAME = os.environ['DB_NAME']
    except KeyError:
        raise RuntimeError('DB_NAME not found in environment')

    POOL = Pool(DB_NAME)
    POOL.init()

    with Transaction().start(DB_NAME, 1, context={}) as txn:
        Product = Pool().get('product.product')

        rename_string_to_display_name()

        if ensure_core_module_is_installed() is True:

            attribute_kv_map = copy_selection_options()
            for product in Product.search([]):
                validate_and_copy_attributes(product, attribute_kv_map)

        txn.cursor.commit()
