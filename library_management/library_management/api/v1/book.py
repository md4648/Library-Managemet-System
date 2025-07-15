import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def create_book(**kwargs):
    try:
        doc = frappe.get_doc(
            {
                "doctype": "Book",
                "title": kwargs.get("title"),
                "author": kwargs.get("author"),
                "isbn": kwargs.get("isbn"),
                "publish_date": kwargs.get("publish_date"),
                "total_copy": kwargs.get("total_copy"),
                "available_copy": kwargs.get("available_copy"),
            }
        )
        doc.insert()
        frappe.db.commit()
        return {"message": f"📘 '{doc.title}' created successfully!"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Book API Failed")
        raise frappe.ValidationError(_("Failed to create book: ") + str(e))


@frappe.whitelist(allow_guest=True)
def get_books():
    """
    Retrieve a list of all books.
    """
    books = frappe.get_all(
        "Book",
        fields=[
            "name",
            "title",
            "author",
            "isbn",
            "publish_date",
            "total_copy",
            "available_copy",
        ],
    )
    return {"books": books}


@frappe.whitelist(allow_guest=True)
def create_loan():
    """
    API to create a new Loan document.
    - Prevents loaning if the book is already issued.
    """
    data = frappe.request.get_json()

    required_fields = ["book", "member", "loan_date", "return_date"]
    for field in required_fields:
        if not data.get(field):
            frappe.throw(_("Field {0} is required.").format(field))

    book_doc = frappe.get_doc("Book", data.get("book"))
    if book_doc.status == "Issued":
        frappe.throw(_("This book is already issued. Please return it first."))

    loan_doc = frappe.get_doc(
        {
            "doctype": "Loan",
            "book": data.get("book"),
            "member": data.get("member"),
            "loan_date": data.get("loan_date"),
            "return_date": data.get("return_date"),
            "select_from_reservation": data.get("select_from_reservation") == 1,
            "reservation_id": data.get("reservation_id") or None,
            "status": "On Loan",
        }
    )

    loan_doc.insert()
    loan_doc.submit()

    return {"message": _("Loan created successfully."), "loan_name": loan_doc.name}


@frappe.whitelist()
def get_loans():
    """
    Retrieve a list of loans belonging to the currently logged-in member only.
    - Maps the logged-in user to their associated Member record.
    - Filters loans by that Member.
    - Respects Frappe's permission system.
    """

    user = frappe.session.user

    member_name = frappe.db.get_value("Member", {"user": user}, "name")
    if not member_name:
        frappe.throw(
            "You are not linked to any Member record. Please contact the librarian."
        )

    loans = frappe.get_list(
        "Loan",
        filters={"member": member_name},
        fields=[
            "name",
            "book",
            "member",
            "loan_date",
            "return_date",
            "status",
        ],
    )

    return {"loans": loans}


@frappe.whitelist()
def reserve_book(book, member, reservation_date=None):
    user = frappe.session.user

    if not frappe.db.exists("User", user):
        frappe.throw(_("Invalid user"))

    if not frappe.db.exists("Book", book):
        frappe.throw(_("Invalid book"))

    if not frappe.db.exists("Member", member):
        frappe.throw(_("Invalid member"))

    doc = frappe.get_doc(
        {
            "doctype": "Reservation",
            "book": book,
            "member": member,
            "reservation_date": reservation_date or frappe.utils.now_datetime(),
            "user": user,
        }
    )
    doc.insert()
    frappe.db.commit()

    return {"message": "Reservation created successfully", "name": doc.name}


@frappe.whitelist()
def delete_book(book_name):
    """
    Deletes a Book document by its name (ID).
    Only allowed for users with delete permission on Book.
    """
    if not book_name:
        frappe.throw(_("Book name is required."))

    # Check if the book exists
    if not frappe.db.exists("Book", book_name):
        frappe.throw(_("Book not found: {0}").format(book_name))

    # Permission check
    doc = frappe.get_doc("Book", book_name)
    if not doc.has_permission("delete"):
        frappe.throw(_("You do not have permission to delete this book."))

    # Delete the book
    doc.delete()
    frappe.db.commit()

    return {"message": _("Book deleted successfully."), "book_name": book_name}


@frappe.whitelist()
def get_dashboard_data():
    total_members = frappe.db.count("Member") or 0
    total_books = frappe.db.count("Book") or 0

    on_loan = frappe.db.count("Loan", {"status": "On Loan"}) or 0

    # Overdue: return_date has passed, and status is still "On Loan"
    overdue = frappe.db.count("Loan", {"status": "Overdue"}) or 0

    return {
        "total_members": total_members,
        "total_books": total_books,
        "on_loan": on_loan,
        "overdue": overdue,
    }
