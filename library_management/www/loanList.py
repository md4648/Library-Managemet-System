import frappe


def get_context(context):
    # pass csrf token
    context.csrf_token = frappe.sessions.get_csrf_token()
    context.loans = frappe.get_list(
        "Loan",
        fields=[
            "name",
            "book",
            "member",
            "loan_date",
            "return_date",
            "status",
        ],
    )

    # Add user roles
    if frappe.session.user != "Guest":
        context.user_roles = frappe.get_roles(frappe.session.user)
    else:
        context.user_roles = []
