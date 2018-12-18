import frappe

@frappe.whitelist(allow_guest=True)
def get_attributes_and_values(item_code):
    attributes = frappe.db.get_list('Item Variant Attribute',
        fields=['attribute'],
        filters={
            'parenttype': 'Item',
            'parent': item_code
        },
        order_by='idx asc'
    )

    attribute_names = [a.attribute for a in attributes]

    values = frappe.db.get_list('Item Attribute Value',
        fields=['attribute_value', 'parent'],
        filters={
            'parent': ['in', attribute_names]
        }
    )

    out = {}

    for value in values:
        attribute = value.parent
        out[attribute] = out.get(attribute, [])
        out[attribute].append(value.attribute_value)

    return out