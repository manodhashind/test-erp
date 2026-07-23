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


@frappe.whitelist()
def create_user_with_password(email, first_name, last_name=None, password="Constr@2026!"):
    if "System Manager" not in frappe.get_roles(frappe.session.user):
        frappe.throw("Not permitted", frappe.PermissionError)

    if frappe.db.exists("User", email):
        frappe.throw(f"User {email} already exists")

    user = frappe.new_doc("User")
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.send_welcome_email = 0
    user.new_password = password
    user.insert(ignore_permissions=True)

    return {"email": email, "password": password}


@frappe.whitelist()
def get_all_users():
    # Any logged-in user (not Guest) can see the full list — enforced deliberately here,
    # bypassing the normal per-role Read restriction on User.
    if frappe.session.user == "Guest":
        frappe.throw("Not permitted", frappe.PermissionError)

    users = frappe.get_all(
        "User",
        fields=["email", "first_name", "last_name", "enabled"],
        filters={"email": ["not in", ["admin@example.com", "guest@example.com"]]},
        ignore_permissions=True,
    )
    return users