// Copyright (c) 2025, Muluneh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Loan", {
	refresh(frm) {
		const today = frappe.datetime.get_today();

		if (frm.doc.return_date && frm.doc.return_date < today && frm.doc.status !== "Returned") {
			frm.set_value("status", "Overdue");
			frm.save(); // Optional: Automatically save
		}

		if (frm.doc.status != "Returned") {
			frm.add_custom_button("Return", () => {
				frappe.model.set_value("Loan", frm.doc.name, "status", "Returned");

				refresh_field("status");
			});
		}
	},
});
