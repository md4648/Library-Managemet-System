# import frappe


# def get_context(context):
#     # pass csrf token
#     context.csrf_token = frappe.sessions.get_csrf_token()
#     context.books = frappe.get_all(
#         "Book",
#         fields=[
#             "name",
#             "title",
#             "author",
#             "isbn",
#             "publish_date",
#             "total_copy",
#             "available_copy",
#             "status",
#         ],
#     )


import frappe


def get_context(context):
    # Pass CSRF token
    context.csrf_token = frappe.sessions.get_csrf_token()

    # Fetch all books
    context.books = frappe.get_all(
        "Book",
        fields=[
            "name",
            "title",
            "author",
            "isbn",
            "publish_date",
            "total_copy",
            "available_copy",
            "status",
        ],
    )

    # Add user roles
    if frappe.session.user != "Guest":
        context.user_roles = frappe.get_roles(frappe.session.user)
    else:
        context.user_roles = []
