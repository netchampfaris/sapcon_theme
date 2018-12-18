$(() => {
	$('.btn-configure').on('click', (e) => {
		const { itemCode, itemName } = $(e.target).data();
		configure_item(itemCode, itemName);
	});
});

function configure_item(item_code, item_name) {
	get_attributes(item_code)
		.then(attribute_data => {
			const fields =
				Object.keys(attribute_data)
					.map(attribute_name => {
						return {
							fieldtype: 'Select',
							label: attribute_name,
							options: attribute_data[attribute_name]
						}
					})
			const d = new frappe.ui.Dialog({
				title: 'Configure ' + item_name,
				fields
			})
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
