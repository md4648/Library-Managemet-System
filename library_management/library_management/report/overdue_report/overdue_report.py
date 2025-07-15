import frappe
from frappe import _, utils

def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	return [
		{"label": _("Book"), "fieldname": "book", "fieldtype": "Link", "options": "Book", "width": 200},
		{"label": _("Book Title"), "fieldname": "book_title", "fieldtype": "Data", "width": 200},
		{"label": _("Member"), "fieldname": "member", "fieldtype": "Link", "options": "Member", "width": 150},
		{"label": _("Member Name"), "fieldname": "member_name", "fieldtype": "Data", "width": 180},
		{"label": _("Return Date"), "fieldname": "return_date", "fieldtype": "Date", "width": 120},
		{"label": _("Days Overdue"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
	]


def get_data():
	today = utils.nowdate()
	loans = frappe.get_all("Loan",
		filters={
			"status": "Overdue",
			"return_date": ["<", today]
		},
		fields=["book", "member", "loan_date", "return_date"],
		order_by="return_date asc"
	)

	data = []
	for loan in loans:
		book_title = frappe.db.get_value("Book", loan.book, "title")
		member_name = frappe.db.get_value("Member", loan.member, "full_name")
		days_overdue = (utils.date_diff(today, loan.return_date))

		data.append({
			"book": loan.book,
			"book_title": book_title,
			"member": loan.member,
			"member_name": member_name,
			"return_date": loan.return_date,
			"days_overdue": days_overdue
		})

	return data
