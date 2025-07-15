// Copyright (c) 2025, Muluneh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book", {
	refresh(frm) {
		if (frm.doc.available_copy <= 0) {
			frm.set_value("status", "Issued");
		} else {
			frm.set_value("status", "Available");
		}
		frm.save();
	},
});
