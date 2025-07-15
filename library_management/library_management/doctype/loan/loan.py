# Copyright (c) 2025, Muluneh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class Loan(Document):
    def on_submit(self):
        book = frappe.get_doc("Book", self.book)

        if self.status == "On Loan" and book.available_copy > 0:
            book.available_copy -= 1
            book.save()
            if book.available_copy == 0:
                book.status = "Issued"
                book.save()

    def validate(self):
        book = frappe.get_doc("Book", self.book)
        if book.status == "Issued":
            frappe.throw(
                "This book is already Issued. Please return it before issuing again."
            )

    def on_update_after_submit(self):
        book = frappe.get_doc("Book", self.book)

        if self.status == "Returned":
            book.status = "Available"
            book.available_copy += 1
            book.save()

            # Find the earliest unfulfilled reservation
            # reservations = frappe.get_all("Reservation",
            # 	filters={
            # 		"book": self.book,
            # 		"workflow_state": "Reserved"
            # 	},
            # 	order_by="reservation_date asc",
            # 	limit=1
            # )

            # if reservations:
            # 	frappe.throw("This book is already reserved. Please fulfill the reservation before returning it.")
            # 	reservation = frappe.get_doc("Reservation", reservations[0].name)
            # 	reservation.status = "Available"
            # 	reservation.fulfilled_on = now_datetime()
            # 	reservation.save(ignore_permissions=True)
