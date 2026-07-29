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
    frappe.flags.in_import = True
    try:
        user.insert(ignore_permissions=True)
    finally:
        frappe.flags.in_import = False

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

import re


# ─────────────────────────────────────────────────────────────
# Internal data helpers (shared by tools + chat engine)
# ─────────────────────────────────────────────────────────────

def _base_filters():
    return {"name": ["not in", ["Administrator", "Guest"]]}


def _list_users(enabled=None):
    filters = _base_filters()
    if enabled is not None:
        filters["enabled"] = 1 if enabled else 0
    return frappe.get_all(
        "User",
        fields=["email", "first_name", "last_name", "enabled", "creation"],
        filters=filters,
        order_by="creation desc",
        ignore_permissions=True,
    )


def _search_users(term):
    if not term:
        return []
    return frappe.get_all(
        "User",
        fields=["email", "first_name", "last_name", "enabled"],
        filters=_base_filters(),
        or_filters=[
            ["first_name", "like", f"%{term}%"],
            ["last_name", "like", f"%{term}%"],
            ["email", "like", f"%{term}%"],
        ],
        ignore_permissions=True,
    )


def _require_admin():
    if "System Manager" not in frappe.get_roles(frappe.session.user):
        frappe.throw("Not permitted", frappe.PermissionError)


# ─────────────────────────────────────────────────────────────
# Whitelisted tool functions (spec-required standalone endpoints)
# ─────────────────────────────────────────────────────────────

@frappe.whitelist()
def get_active_users():
    return _list_users(enabled=True)


@frappe.whitelist()
def get_disabled_users():
    return _list_users(enabled=False)


@frappe.whitelist()
def search_user(name):
    return _search_users(name)


@frappe.whitelist()
def update_user(email, first_name=None, last_name=None):
    _require_admin()
    if not frappe.db.exists("User", email):
        frappe.throw(f"No user found with email {email}")
    doc = frappe.get_doc("User", email)
    if first_name:
        doc.first_name = first_name
    if last_name:
        doc.last_name = last_name
    doc.save(ignore_permissions=True)
    return {"email": email, "first_name": doc.first_name, "last_name": doc.last_name}


@frappe.whitelist()
def delete_user(email):
    _require_admin()
    if not frappe.db.exists("User", email):
        frappe.throw(f"No user found with email {email}")
    frappe.delete_doc("User", email, ignore_permissions=True, force=True)
    return {"deleted": email}


@frappe.whitelist()
def enable_user(email):
    _require_admin()
    if not frappe.db.exists("User", email):
        frappe.throw(f"No user found with email {email}")
    frappe.db.set_value("User", email, "enabled", 1)
    return {"email": email, "enabled": True}


@frappe.whitelist()
def disable_user(email):
    _require_admin()
    if not frappe.db.exists("User", email):
        frappe.throw(f"No user found with email {email}")
    frappe.db.set_value("User", email, "enabled", 0)
    return {"email": email, "enabled": False}


@frappe.whitelist()
def user_statistics():
    all_users = _list_users()
    active = [u for u in all_users if u.enabled]
    disabled = [u for u in all_users if not u.enabled]
    admins = frappe.get_all(
        "Has Role",
        filters={"role": "System Manager", "parenttype": "User"},
        pluck="parent",
    )
    admins = [a for a in admins if a not in ("Administrator", "Guest")]
    recent = sorted(all_users, key=lambda u: u.creation, reverse=True)[:5]
    return {
        "total": len(all_users),
        "active": len(active),
        "disabled": len(disabled),
        "admins": len(admins),
        "recent": [{"email": u.email, "first_name": u.first_name} for u in recent],
    }


# ─────────────────────────────────────────────────────────────
# Chat / intent-detection engine
# ─────────────────────────────────────────────────────────────

EMAIL_RE = re.compile(r"[\w\.\-]+@[\w\.\-]+\.\w+")
STOPWORDS = {
    "show", "the", "user", "users", "please", "all", "list", "display", "who",
    "is", "for", "find", "search", "locate", "delete", "remove", "enable",
    "activate", "disable", "deactivate", "create", "add", "update", "edit",
    "change", "rename", "him", "her", "them", "a", "an", "of", "to", "named",
    "employee",
}


def _extract_name(msg):
    words = re.sub(r"[?.!,]", "", msg).split()
    names = [w for w in words if w[:1].isupper() and w.lower() not in STOPWORDS]
    return " ".join(names) if names else None


def _extract_email(msg):
    m = EMAIL_RE.search(msg)
    return m.group(0) if m else None


def _format_user_line(u):
    name = f"{u.get('first_name', '')} {u.get('last_name', '') or ''}".strip()
    return f"• {name or u['email']} ({u['email']})"


def _list_reply(users, label):
    if not users:
        return f"There are no {label} users right now."
    lines = "\n".join(_format_user_line(u) for u in users[:10])
    more = f"\n\n…and {len(users) - 10} more." if len(users) > 10 else ""
    return f"There are {len(users)} {label} users.\n\n{lines}{more}"


@frappe.whitelist()
def process_chat_message(message, context=None):
    """Single entrypoint: does intent detection, calls the right tool, formats a reply.
    `context` carries conversation memory (last mentioned user, pending multi-step actions)
    since this endpoint itself is stateless between calls."""
    ctx = frappe.parse_json(context) if isinstance(context, str) else (context or {})
    pending = ctx.get("pending")
    last_user = ctx.get("last_user")
    msg = (message or "").strip()
    lower = msg.lower()

    # ── Continue a pending multi-step create ──────────────────
    if pending and pending.get("type") == "create_user":
        return _continue_create(msg, pending)

    # ── Continue a pending delete confirmation ─────────────────
    if pending and pending.get("type") == "confirm_delete":
        if re.match(r"^(yes|y|confirm|yeah|ok|okay)\b", lower):
            try:
                delete_user(pending["email"])
                return _reply(f"Done — {pending.get('display', pending['email'])} has been deleted.",
                              last_user=None, pending=None)
            except Exception as e:
                return _reply(f"Couldn't delete that user: {e}", last_user=last_user, pending=None)
        else:
            return _reply("Okay, cancelled — no changes made.", last_user=last_user, pending=None)

    # ── Greeting ────────────────────────────────────────────────
    if re.search(r"\b(hi|hello|hey)\b", lower):
        return _reply(
            "Hello 👋 I'm your User Management Assistant.\n\n"
            "I can help you:\n• View users\n• Search users\n• Create users\n"
            "• Edit users\n• Delete users\n• Enable or disable users\n• Show user statistics\n\n"
            'Try asking: "Show active users"',
            last_user=last_user, pending=None,
        )

    # ── Help ────────────────────────────────────────────────────
    if re.search(r"help|what can you do|show commands", lower):
        return _reply(
            "Here's what I can do:\n\n"
            "• \"Show all users\" — list everyone\n"
            "• \"Show active users\" / \"Show disabled users\"\n"
            "• \"Find Mano\" — search by name\n"
            "• \"Create user Mano Doe mano@example.com\"\n"
            "• \"Update Mano's last name to Doe\"\n"
            "• \"Delete Mano\" (asks for confirmation first)\n"
            "• \"Enable/Disable Mano\"\n"
            "• \"User statistics\" — quick dashboard summary",
            last_user=last_user, pending=None,
        )

    # ── Statistics ──────────────────────────────────────────────
    if re.search(r"statistic|summary|dashboard", lower):
        stats = user_statistics()
        recent = ", ".join(r["first_name"] or r["email"] for r in stats["recent"]) or "none"
        return _reply(
            f"Here's the current user summary:\n\n"
            f"• Total users: {stats['total']}\n"
            f"• Active: {stats['active']}\n"
            f"• Disabled: {stats['disabled']}\n"
            f"• Administrators: {stats['admins']}\n"
            f"• Recently added: {recent}",
            last_user=last_user, pending=None,
        )

    # ── Active / disabled / all users ──────────────────────────
    if re.search(r"active users|enabled users|who is enabled", lower):
        return _reply(_list_reply(get_active_users(), "active"), last_user=last_user, pending=None)

    if re.search(r"disabled users|inactive users", lower):
        return _reply(_list_reply(get_disabled_users(), "disabled"), last_user=last_user, pending=None)

    if re.search(r"all users|list users|show users|who are the users", lower):
        return _reply(_list_reply(_list_users(), "total"), last_user=last_user, pending=None)

    # ── Search ──────────────────────────────────────────────────
    if re.search(r"^(find|search|locate)\b", lower):
        name = _extract_name(msg)
        results = _search_users(name) if name else []
        if not results:
            return _reply(f"I couldn't find any user named {name or 'that'}.", last_user=last_user, pending=None)
        if len(results) > 1:
            lines = "\n".join(_format_user_line(u) for u in results)
            return _reply(f"I found {len(results)} users matching \"{name}\":\n\n{lines}\n\nWhich one did you mean?",
                          last_user=last_user, pending=None)
        u = results[0]
        return _reply(f"Found {u['first_name']} {u['last_name'] or ''}. ({u['email']})",
                      last_user={"email": u["email"], "first_name": u["first_name"], "last_name": u["last_name"]},
                      pending=None)

    # ── Create ──────────────────────────────────────────────────
    if re.search(r"\b(create|add)\b", lower) and ("user" in lower or _extract_email(msg) or _extract_name(msg)):
        return _start_create(msg)

    # ── Delete ──────────────────────────────────────────────────
    if re.search(r"\b(delete|remove)\b", lower):
        return _start_delete(msg, last_user)

    # ── Enable / Disable ───────────────────────────────────────
    if re.search(r"\b(enable|activate)\b", lower):
        return _do_toggle(msg, last_user, enable=True)

    if re.search(r"\b(disable|deactivate)\b", lower):
        return _do_toggle(msg, last_user, enable=False)

    # ── Update ──────────────────────────────────────────────────
    if re.search(r"\b(update|edit|change|rename)\b", lower):
        return _start_update(msg, last_user)

    # ── Fallback ────────────────────────────────────────────────
    return _reply(
        "I'm not sure I understood that. Try \"help\" to see what I can do, "
        "or ask something like \"show active users\".",
        last_user=last_user, pending=None,
    )


def _reply(text, last_user=None, pending=None, data=None):
    return {"reply": text, "data": data, "context": {"last_user": last_user, "pending": pending}}


def _resolve_target(msg, last_user):
    """Resolve which user a command refers to: explicit email > explicit name > pronoun via last_user."""
    email = _extract_email(msg)
    if email:
        return email, None
    name = _extract_name(msg)
    if name:
        results = _search_users(name)
        return None, results
    if re.search(r"\bhim\b|\bher\b|\bthem\b", msg.lower()) and last_user:
        return last_user["email"], None
    return None, None


def _start_delete(msg, last_user):
    email, candidates = _resolve_target(msg, last_user)
    if not email and candidates:
        if len(candidates) == 1:
            email = candidates[0]["email"]
        elif len(candidates) > 1:
            lines = "\n".join(_format_user_line(u) for u in candidates)
            return _reply(f"I found {len(candidates)} matching users:\n\n{lines}\n\nWhich one did you mean?",
                          last_user=last_user, pending=None)
    if not email:
        return _reply("Who would you like to delete? Please give me a name or email.",
                      last_user=last_user, pending=None)
    if not frappe.db.exists("User", email):
        return _reply(f"I couldn't find a user with email {email}.", last_user=last_user, pending=None)
    u = frappe.get_doc("User", email)
    display = f"{u.first_name} {u.last_name or ''}".strip()
    return _reply(
        f"You're about to delete:\n{display}\n{email}\n\nType \"yes\" to confirm, or anything else to cancel.",
        last_user=last_user,
        pending={"type": "confirm_delete", "email": email, "display": display},
    )


def _do_toggle(msg, last_user, enable):
    email, candidates = _resolve_target(msg, last_user)
    if not email and candidates:
        if len(candidates) == 1:
            email = candidates[0]["email"]
        elif len(candidates) > 1:
            lines = "\n".join(_format_user_line(u) for u in candidates)
            return _reply(f"I found {len(candidates)} matching users:\n\n{lines}\n\nWhich one did you mean?",
                          last_user=last_user, pending=None)
    if not email:
        action = "enable" if enable else "disable"
        return _reply(f"Who would you like to {action}? Please give me a name or email.",
                      last_user=last_user, pending=None)
    try:
        if enable:
            enable_user(email)
        else:
            disable_user(email)
        u = frappe.get_doc("User", email)
        display = f"{u.first_name} {u.last_name or ''}".strip()
        action_word = "enabled" if enable else "disabled"
        return _reply(f"{display} has been {action_word}.",
                      last_user={"email": email, "first_name": u.first_name, "last_name": u.last_name},
                      pending=None)
    except Exception as e:
        return _reply(f"Couldn't do that: {e}", last_user=last_user, pending=None)


def _start_update(msg, last_user):
    email, candidates = _resolve_target(msg, last_user)
    if not email and candidates and len(candidates) == 1:
        email = candidates[0]["email"]
    if not email:
        return _reply("Who would you like to update? Please give me a name or email first.",
                      last_user=last_user, pending=None)

    new_name = None
    m = re.search(r"(?:last name|lastname)\s*(?:to|=|:)?\s*([A-Z][a-zA-Z]*)", msg)
    field = "last_name"
    if not m:
        m = re.search(r"(?:first name|firstname)\s*(?:to|=|:)?\s*([A-Z][a-zA-Z]*)", msg)
        field = "first_name"
    if m:
        new_name = m.group(1)

    if not new_name:
        return _reply(
            "What would you like to change, and to what? "
            "e.g. \"change last name to Doe\"",
            last_user={"email": email}, pending=None,
        )

    try:
        kwargs = {field: new_name}
        update_user(email, **kwargs)
        u = frappe.get_doc("User", email)
        display = f"{u.first_name} {u.last_name or ''}".strip()
        return _reply(f"Updated — {display} ({email}).",
                      last_user={"email": email, "first_name": u.first_name, "last_name": u.last_name},
                      pending=None)
    except Exception as e:
        return _reply(f"Couldn't update that user: {e}", last_user=last_user, pending=None)


def _start_create(msg):
    email = _extract_email(msg)
    name = _extract_name(msg)
    parts = name.split() if name else []
    first = parts[0] if parts else None
    last = " ".join(parts[1:]) if len(parts) > 1 else None

    if first and email:
        return _finish_create(first, last, email)

    pending = {"type": "create_user", "first_name": first, "last_name": last, "email": email}
    missing = []
    if not first:
        missing.append("first name")
    if not email:
        missing.append("email")
    return _reply(f"Sure — what's the new user's {' and '.join(missing)}?",
                  last_user=None, pending=pending)


def _continue_create(msg, pending):
    email = _extract_email(msg) or pending.get("email")
    name = _extract_name(msg)
    first = pending.get("first_name") or (name.split()[0] if name else None)
    last = pending.get("last_name") or (" ".join(name.split()[1:]) if name and len(name.split()) > 1 else None)

    if first and email:
        return _finish_create(first, last, email)

    missing = []
    if not first:
        missing.append("first name")
    if not email:
        missing.append("email")
    new_pending = {"type": "create_user", "first_name": first, "last_name": last, "email": email}
    return _reply(f"Got it. I still need the {' and '.join(missing)}.", last_user=None, pending=new_pending)


def _finish_create(first, last, email):
    try:
        result = create_user_with_password(email=email, first_name=first, last_name=last)
        return _reply(
            f"Created {first} {(last or '').strip()} — {email}\nDefault password: {result['password']}",
            last_user={"email": email, "first_name": first, "last_name": last},
            pending=None,
        )
    except Exception as e:
        return _reply(f"Couldn't create that user: {e}", last_user=None, pending=None)