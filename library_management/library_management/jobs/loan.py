# Overdue Notifications – “As the system, I want to email members when their loans
# become overdue so that they return books promptly.”
# create function to send overdue EMAIL

import frappe
from frappe import _
from frappe.utils import nowdate


@frappe.whitelist(allow_guest=True)
def send_overdue_notifications():
    """
    Send overdue notifications to members with overdue loans.

    This function checks for loans that are overdue and sends an email notification
    to the respective members. It is accessible to guests.
    """
    overdue_loans = frappe.get_all(
        "Loan",
        filters={"return_date": ["<", nowdate()], "status": "On Loan"},
        fields=["name", "member", "book"],
    )

    for loan in overdue_loans:
        member = frappe.get_doc("Member", loan.member)
        book = frappe.get_doc("Book", loan.book)

        subject = _("Overdue Loan Notification")
        message = _(
            "Dear {0},<br><br>"
            "This is a reminder that the book '{1}' is overdue. "
            "Please return it as soon as possible.<br><br>"
            "Thank you!<br>"
            "Library Management System"
        ).format(member.name, book.title)

        frappe.sendmail(recipients=member.email, subject=subject, message=message)
        # Optionally, you can update the loan status or log the notification
        frappe.db.set_value("Loan", loan.name, "status", "Overdue")

    frappe.db.commit()  # Commit the changes to the database

    return {"message": _("Overdue notifications sent successfully.")}
