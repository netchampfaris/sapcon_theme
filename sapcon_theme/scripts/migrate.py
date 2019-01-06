import frappe

def execute():
    '''
    There exists two items who have the same item_code.
    Since item_code column is unique, migrate breaks.
    '''

    frappe.db.sql('''
        update tabItem
        set item_code=name
        where item_code='SLW-R-SNSR-PCB5S4-SQW-RCB5S4-830-AU1-REF-F20S4-ROP-SS4-P-10T-10H50H';
    ''')

def set_product_type():
    values = {
        'Point Level': ['CE', 'ELIXIR', 'ETU', 'RP', 'SLA_B', 'SLA_D', 'SLA_S', 'SLA_T', 'SLC_S', 'SLC_T', 'SLM', 'SLW', 'VITAL', 'VS'],
        'Flow': ['MPLOH', 'MPROF', 'DT'],
        'Continuous Level Transmitter': ['CAPVEL_ICT', 'CAPVEL_LP', 'ICE_P', 'MPILC', 'STLR', 'VAT'],
        'Speed Monitor': ['SSSI']
    }

    for value, item_codes in values.items():
        set_filter_properties(item_codes, 'product_type', value)

def set_sensing_type():
    values = {
        'Admittance': ['CE', 'SLA_B', 'SLA_D', 'SLA_S', 'SLA_T'],
        'Capacitance': ['CAPVEL_ICT', 'CAPVEL_LP', 'ICE_P', 'SLC_S', 'SLC_T', 'VAT', 'DT'],
        'Conductive': ['SLW'],
        'Electromechanical': ['RP'],
        'Open Channel Monitoring': ['MPLOH', 'MPROF'],
        'Pressure': ['STLR'],
        'Transmitter De-oiled Toaster Application': ['DT'],
        'Vibrating Fork': ['ELIXIR', 'ETU', 'SLM', 'VITAL'],
        'Vibrating Rod': ['VS']
    }

    for value, item_codes in values.items():
        set_filter_properties(item_codes, 'sensing_type', value)

def set_filter_properties(item_codes, field, value):
    # TODO: Update modified timestamp
    values = [value] + item_codes
    in_query = ', '.join(['%s'] * len(item_codes))

    frappe.db.sql('''
        update tabItem
        set {field} = %s
        where name in ({in_query})
    '''.format(field=field, in_query=in_query), values, debug=1)

def add_indexes():
    frappe.db.add_index('Item', ['product_type'])
    frappe.db.add_index('Item', ['sensing_type'])
    frappe.db.add_index('Item', ['variant_of', 'name'])
    frappe.db.add_index('Item Variant Attribute', ['attribute', 'attribute_value', 'parent'])
    frappe.db.add_index('Item Variant Attribute', ['variant_of'])
