import frappe, json

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

	return out, attribute_names

@frappe.whitelist(allow_guest=True)
def get_item_with_attributes(template_item_code, attribute_dict):

	if isinstance(attribute_dict, frappe.string_types):
		attribute_dict = json.loads(attribute_dict)

	attribute_data = get_attributes_and_values(template_item_code)[0]

	attribute_value_len_map = {}
	for attribute, attribute_values in attribute_data.iteritems():
		attribute_value_len_map[attribute] = len(attribute_values)

	attribute_list = sorted(attribute_dict.items(),
		key = lambda x: attribute_value_len_map[x[0]],
		reverse=True)

	print(attribute_value_len_map)
	print(attribute_list)

	items = []

	for attribute, attribute_value in attribute_list:
		where =  '( attribute = %s and attribute_value = %s )'
		values = [attribute, attribute_value]

		query = '''
			select
				parent
			from `tabItem Variant Attribute`
			where
				({where})
			group by parent
		'''.format(where=where)

		item_codes = set([r[0] for r in frappe.db.sql(query, values)])
		items.append(item_codes)

	res = set.intersection(*items)

	return res
