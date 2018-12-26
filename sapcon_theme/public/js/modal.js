frappe.get_modal = function(title, content) {
	return $(
		`<div class="modal" tabindex="-1" role="dialog">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">${title}</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					<div class="modal-body py-4">
						${content}
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-primary"></button>
					</div>
				</div>
			</div>
		</div>`
	);
};

frappe.ui.Dialog.prototype.get_primary_btn = function() {
	return this.$wrapper.find(".modal-footer .btn-primary");
}