import frappe


def get_context(context):

    # Add user roles
    context.current_path = frappe.local.request.path
