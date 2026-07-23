import frappe

@frappe.whitelist()
def get_current_user_info():
    user = frappe.session.user
    roles = frappe.get_roles(user)
    return {
        "user": user,
        "is_admin": "System Manager" in roles,
        "roles": roles,
    }