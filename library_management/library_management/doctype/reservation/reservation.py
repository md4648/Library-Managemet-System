# Copyright (c) 2025, Muluneh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Reservation(Document):
	def validate(self):
		book=frappe.get_doc("Book",self.book)
		if book.available_copy <= 0:
			frappe.throw("No available copies of this book. Please reserve it first.")
