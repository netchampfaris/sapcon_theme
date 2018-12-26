$(() => {
	$('.btn-configure').on('click', (e) => {
		const { itemCode, itemName } = $(e.target).data();
		configure_item(itemCode, itemName);
	});
});

function configure_item(item_code, item_name) {
	get_attributes(item_code)
		.then(([attribute_data, attribute_order]) => {
			const fields = attribute_order.map(attribute_name => {
				return {
					fieldtype: 'Select',
					label: attribute_name,
					fieldname: attribute_name,
					options: attribute_data[attribute_name]
				}
			});
			const d = new frappe.ui.Dialog({
				title: 'Configure ' + item_name,
				fields,
				primary_action_label: __('Submit'),
				primary_action(values) {
					console.log(values);
					frappe.call('sapcon_theme.templates.generators.product_finder.get_item_with_attributes', {
						attribute_dict: values,
						template_item_code: item_code
					}).then(r => {
						console.log(r)
					})
				}
			});
			d.show();
		})
}

function get_attributes(item_code) {
	return new Promise(resolve => {
		frappe.call('sapcon_theme.templates.generators.product_finder.get_attributes_and_values', {
			item_code
		})
		.then(r => resolve(r.message))
	})
}
