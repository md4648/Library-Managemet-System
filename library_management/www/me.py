import frappe


def get_context(context):

    # Add user roles
    if frappe.session.user != "Guest":
        context.user_roles = frappe.get_roles(frappe.session.user)
    else:
        context.user_roles = []
