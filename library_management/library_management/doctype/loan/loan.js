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

		async function getReservation() {
			try {
				if (frm.doc.select_from_reservation == 1 || frm.doc.docstatus == 1) {
					frappe.model.set_value(
						"Reservation",
						frm.doc.reservation_id,
						"workflow_state",
						"Completed"
					);
				}
			} catch (error) {
				console.error("Error fetching document:", error);
			}
		}
		if (frm.doc.select_from_reservation == 1) {
			getReservation(frm);
		}
	},
	select_from_reservation(frm) {
		if (frm.doc.select_from_reservation == 1) {
			frm.set_df_property("book", "read_only", 1);
			frm.set_df_property("member", "read_only", 1);
		} else {
			frm.set_df_property("book", "read_only", 0);
			frm.set_df_property("member", "read_only", 0);
			frm.set_value("reservation_id", null);
		}
	},

	reservation_id(frm) {
		async function getReservation() {
			try {
				const reservation = await frappe.db.get_doc("Reservation", frm.doc.reservation_id);

				frm.set_value("book", reservation.book);
				frm.set_value("member", reservation.member);
			} catch (error) {
				console.error("Error fetching document:", error);
			}
		}
		getReservation(frm);
	},
});
