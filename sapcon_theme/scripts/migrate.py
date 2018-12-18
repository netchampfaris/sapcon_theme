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
