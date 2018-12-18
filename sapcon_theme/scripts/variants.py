import frappe


def set_variant_of():
	templates = get_item_templates()

	for template in templates:
		print('Processing', template)

		frappe.db.sql('''
			update tabItem
			set variant_of="{template}",
				variant_based_on="Item Attribute"
			where name like "{template}-%"
		'''.format(template=template))

		frappe.db.commit()


def add_item_attributes():
	import time
	start = time.time()
	item_variants = get_item_variants(0, 10**5)
	for item in item_variants:
		try:
			print('Processing', item)
			add_item_attributes_in_variant(item)
		except Exception as e:
			log_error(item, e)

	print(time.time() - start)


def get_attr_dict():
	attributes = frappe.db.sql('''
		select `tabItem Attribute`.attribute_name, `tabItem Attribute Value`.attribute_value, `tabItem Attribute Value`.abbr
		FROM `tabItem Attribute Value` INNER JOIN `tabItem Attribute`
		where `tabItem Attribute Value`.parent = `tabItem Attribute`.attribute_name
	''')
	attr_dict = {}

	for attribute in attributes:
		attr_dict[attribute[2]] = {'attribute':attribute[0], 'attribute_value':attribute[1]}
	return attr_dict


def get_item_variants(start=0, page_length=100):
	templates = get_item_templates()

	items = frappe.db.sql('''
		SELECT item_code from tabItem
		where item_group like "Product-%"
		limit {start}, {page_length}
	'''.format(start=start, page_length=page_length), as_list=1)

	items = [item[0] for item in items]
	return [item for item in items if item.startswith(tuple(templates))]

def get_item_templates():
	templates = frappe.db.sql('SELECT name from tabItem where item_group like "Product Templates"', as_list=1)
	templates = [t[0] for t in templates]
	return templates

attr_dict = get_attr_dict()

def add_item_attributes_in_variant(item):
	if is_already_done(item):
		print('already done', item)
		return

	child_attributes = []
	item_attribute_values = item.split('-')[1:]

	for index, item_attribute_value in enumerate(item_attribute_values):
		try:
			child_attribute = frappe._dict(attr_dict[item_attribute_value])
		except:
			log_error(item, 'Could not find attribute name for value ' + item_attribute_value)
			continue

		child_attribute.creation = frappe.utils.now()
		child_attribute.docstatus = 0
		child_attribute.from_range = 0
		child_attribute.idx = index + 1
		child_attribute.increment = 0
		child_attribute.modified_by = child_attribute.owner = "Administrator"
		child_attribute.name = frappe.generate_hash('Item Variant Attribute', 10)
		child_attribute.modified = child_attribute.creation
		child_attribute.numeric_values = 0
		child_attribute.parent = item
		child_attribute.parentfield = "attributes"
		child_attribute.parenttype = "Item"
		child_attribute.to_range = 0
		child_attributes.append(child_attribute)


	keys = ', '.join(child_attributes[0].keys())

	values = ''
	for child_attribute in child_attributes:
		values += '(' + ', '.join(["%s"] * len(child_attribute.values())) + '), '

	values = values[:-2]

	attribute_values = []
	for child_attribute in child_attributes:
		for attr_value in child_attribute.values():
			attribute_values.append(attr_value)


	query = "INSERT INTO `tabItem Variant Attribute` ({keys}) VALUES {values}".format(keys=keys, values=values)
	#print(attribute_values)
	#print(query)
	frappe.db.sql(query, attribute_values)
	add_to_completed(item)


def add_to_completed(item):
	with open('done.txt', 'a+') as f:
		f.write("{item}\n".format(item=item))

def log_error(item, traceback):
	with open('error.txt', 'a+') as f:
		f.write("{0}\n{1}\n\n".format(item, traceback))

def is_already_done(item):
	try:
		with open('done.txt', 'r') as f:
			return item in f.read()
	except:
		return False
