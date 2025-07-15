import frappe


def get_context(context):
    # Get the book name from the URL (book name will be passed as part of the URL)
    book_name = frappe.form_dict.get("name")

    if not book_name:
        frappe.throw("book name is missing in the URL.")

    # Fetch the book document using its name
    try:
        book = frappe.get_doc("Book", book_name)
    except frappe.DoesNotExistError:
        frappe.throw(f"book with name '{book_name}' does not exist.")

    # Pass the book document to the context
    context.doc = book
    return context
