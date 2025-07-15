# Copyright (c) 2025, Muluneh and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters: dict | None = None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns() -> list[dict]:
	return [
		{"label": _("Book"), "fieldname": "book", "fieldtype": "Link", "options": "Book", "width": 200},
		{"label": _("Book Title"), "fieldname": "book_title", "fieldtype": "Data", "width": 200},
		{"label": _("Member"), "fieldname": "member", "fieldtype": "Link", "options": "Member", "width": 150},
		{"label": _("Member Name"), "fieldname": "member_name", "fieldtype": "Data", "width": 180},
		{"label": _("Loan Date"), "fieldname": "loan_date", "fieldtype": "Date", "width": 120},
		{"label": _("Return Date"), "fieldname": "return_date", "fieldtype": "Date", "width": 120},
	]


def get_data() -> list[dict]:
	# Fetch active loans (not returned yet)
	loans = frappe.get_all("Loan",
		filters={"status": "On Loan"},
		fields=["book", "member", "loan_date", "return_date"],
		order_by="loan_date desc"
	)

	data = []
	for loan in loans:
		book = frappe.db.get_value("Book", loan.book, "title")
		member_name = frappe.db.get_value("Member", loan.member, "full_name")
		data.append({
			"book": loan.book,
			"book_title": book,
			"member": loan.member,
			"member_name": member_name,
			"loan_date": loan.loan_date,
			"return_date": loan.return_date
		})

	return data
