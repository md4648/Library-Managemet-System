// Copyright (c) 2025, Muluneh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Reservation", {
	refresh(frm) {
		frm.set_query("book", function () {
			return {
				filters: {
					status: "Issued",
				},
			};
		});
	},
});
