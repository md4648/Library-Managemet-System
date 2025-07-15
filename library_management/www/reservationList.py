import frappe


def get_context(context):
    # pass csrf token
    context.csrf_token = frappe.sessions.get_csrf_token()
    context.reservations = frappe.get_list(
        "Reservation",
        fields=[
            "name",
            "book",
            "member",
            "reservation_date",
            "workflow_state",
        ],
    )

    # Add user roles
    if frappe.session.user != "Guest":
        context.user_roles = frappe.get_roles(frappe.session.user)
    else:
        context.user_roles = []
