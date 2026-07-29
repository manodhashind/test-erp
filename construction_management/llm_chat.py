import json
import requests
import frappe

from construction_management.api import (
    get_active_users, get_disabled_users, _list_users, _search_users,
    create_user_with_password, update_user, delete_user, enable_user,
    disable_user, user_statistics, _require_admin,
)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:1.5b"

INTENT_PROMPT = """You are an intent classifier for a user-management chat assistant. Given the user's message, respond with ONLY a JSON object (no other text) in this exact shape:

{"intent": "<one of the intents below>", "name": "<name mentioned, or null>", "email": "<email mentioned, or null>", "first_name": "<first name for create, or null>", "last_name": "<last name for create, or null>"}

Valid intents: greeting, help, list_all, list_active, list_disabled, search, create, update, delete, enable, disable, statistics, confirm_yes, confirm_no, unknown

Examples:
"hi" -> {"intent":"greeting","name":null,"email":null,"first_name":null,"last_name":null}
"show active users" -> {"intent":"list_active","name":null,"email":null,"first_name":null,"last_name":null}
"find John" -> {"intent":"search","name":"John","email":null,"first_name":null,"last_name":null}
"delete john@test.com" -> {"intent":"delete","name":null,"email":"john@test.com","first_name":null,"last_name":null}
"yes" -> {"intent":"confirm_yes","name":null,"email":null,"first_name":null,"last_name":null}
"create user John Smith john@test.com" -> {"intent":"create","name":null,"email":"john@test.com","first_name":"John","last_name":"Smith"}

Respond with ONLY the JSON object, nothing else."""


def _call_ollama_json(user_message):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "format": "json",  # forces Ollama to constrain output to valid JSON
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=30)
    resp.raise_for_status()
    content = resp.json().get("message", {}).get("content", "{}")
    try:
        return json.loads(content)
    except Exception:
        return {"intent": "unknown"}


def _format_user_line(u):
    name = f"{u.get('first_name', '')} {u.get('last_name') or ''}".strip()
    return f"• {name or u['email']} ({u['email']})"


def _list_reply(users, label):
    if not users:
        return f"There are no {label} users right now."
    lines = "\n".join(_format_user_line(u) for u in users[:15])
    more = f"\n…and {len(users) - 15} more." if len(users) > 15 else ""
    return f"There are {len(users)} {label} users.\n\n{lines}{more}"


@frappe.whitelist()
def process_chat_message_llm(message, context=None):
    """Python owns ALL state (pending confirmations, last-mentioned user).
    The LLM is only ever asked one narrow question: 'what does this message mean?'
    It never controls when an action actually executes — that's fully deterministic."""
    _require_admin()
    ctx = frappe.parse_json(context) if isinstance(context, str) else (context or {})
    pending = ctx.get("pending")
    last_user = ctx.get("last_user")
    msg = (message or "").strip()
    lower = msg.lower()

    # ── Handle a pending confirmation WITHOUT calling the LLM at all — ─────
    # plain yes/no is too important to leave to a small model's guesswork.
    if pending and pending.get("type") == "confirm_delete":
        if lower in ("yes", "y", "yeah", "yep", "confirm", "ok", "okay", "sure"):
            try:
                delete_user(pending["email"])
                return _reply(f"Done — {pending.get('display')} has been deleted.", None, None)
            except Exception as e:
                return _reply(f"Couldn't delete that user: {e}", last_user, None)
        else:
            return _reply("Okay, cancelled — no changes made.", last_user, None)

    try:
        parsed = _call_ollama_json(msg)
    except requests.exceptions.ConnectionError:
        return _reply("The AI service isn't reachable — please check that `ollama serve` is running.",
                      last_user, pending)
    intent = parsed.get("intent", "unknown")

    if intent == "greeting":
        return _reply(
            "Hello 👋 I'm your User Management Assistant.\n\n"
            "I can help you view, search, create, edit, delete, enable, or disable users, "
            "and show statistics.\n\nTry: \"show active users\"",
            last_user, None,
        )
    if intent == "help":
        return _reply(
            "Here's what I can do:\n\n"
            "• \"Show all/active/disabled users\"\n• \"Find John\"\n"
            "• \"Create user John Smith john@example.com\"\n"
            "• \"Delete John\" (I'll ask you to confirm)\n"
            "• \"Enable/Disable John\"\n• \"User statistics\"",
            last_user, None,
        )
    if intent == "list_all":
        return _reply(_list_reply(_list_users(), "total"), last_user, None)
    if intent == "list_active":
        return _reply(_list_reply(get_active_users(), "active"), last_user, None)
    if intent == "list_disabled":
        return _reply(_list_reply(get_disabled_users(), "disabled"), last_user, None)
    if intent == "statistics":
        stats = user_statistics()
        recent = ", ".join(r["first_name"] or r["email"] for r in stats["recent"]) or "none"
        return _reply(
            f"Summary:\n\n• Total: {stats['total']}\n• Active: {stats['active']}\n"
            f"• Disabled: {stats['disabled']}\n• Admins: {stats['admins']}\n• Recent: {recent}",
            last_user, None,
        )
    if intent == "search":
        name = parsed.get("name")
        results = _search_users(name) if name else []
        if not results:
            return _reply(f"I couldn't find any user named {name or 'that'}.", last_user, None)
        if len(results) > 1:
            lines = "\n".join(_format_user_line(u) for u in results)
            return _reply(f"I found {len(results)} matches:\n\n{lines}\n\nWhich one did you mean?", last_user, None)
        u = results[0]
        return _reply(f"Found {u['first_name']} {u['last_name'] or ''}. ({u['email']})",
                      {"email": u["email"], "first_name": u["first_name"], "last_name": u["last_name"]}, None)
    if intent == "delete":
        email = parsed.get("email") or (last_user and last_user.get("email"))
        if not email:
            return _reply("Who would you like to delete? Please give me a name or email.", last_user, None)
        if not frappe.db.exists("User", email):
            return _reply(f"I couldn't find a user with email {email}.", last_user, None)
        u = frappe.get_doc("User", email)
        display = f"{u.first_name} {u.last_name or ''}".strip()
        return _reply(
            f"You're about to delete:\n{display}\n{email}\n\nType \"yes\" to confirm, or anything else to cancel.",
            last_user, {"type": "confirm_delete", "email": email, "display": display},
        )
    if intent in ("enable", "disable"):
        email = parsed.get("email") or (last_user and last_user.get("email"))
        if not email:
            return _reply(f"Who would you like to {intent}? Please give me a name or email.", last_user, None)
        try:
            (enable_user if intent == "enable" else disable_user)(email)
            u = frappe.get_doc("User", email)
            display = f"{u.first_name} {u.last_name or ''}".strip()
            return _reply(f"{display} has been {intent}d.",
                          {"email": email, "first_name": u.first_name, "last_name": u.last_name}, None)
        except Exception as e:
            return _reply(f"Couldn't do that: {e}", last_user, None)
    if intent == "create":
        email, first, last = parsed.get("email"), parsed.get("first_name"), parsed.get("last_name")
        if not (email and first):
            return _reply("What's the new user's first name and email?", last_user, None)
        try:
            result = create_user_with_password(email=email, first_name=first, last_name=last)
            return _reply(f"Created {first} {last or ''} — {email}\nPassword: {result['password']}",
                          {"email": email, "first_name": first, "last_name": last}, None)
        except Exception as e:
            return _reply(f"Couldn't create that user: {e}", last_user, None)
    if intent == "update":
        email = parsed.get("email") or (last_user and last_user.get("email"))
        if not email:
            return _reply("Who would you like to update?", last_user, None)
        kwargs = {}
        if parsed.get("first_name"):
            kwargs["first_name"] = parsed["first_name"]
        if parsed.get("last_name"):
            kwargs["last_name"] = parsed["last_name"]
        if not kwargs:
            return _reply("What would you like to change, and to what?", {"email": email}, None)
        try:
            update_user(email, **kwargs)
            u = frappe.get_doc("User", email)
            return _reply(f"Updated — {u.first_name} {u.last_name or ''} ({email})",
                          {"email": email, "first_name": u.first_name, "last_name": u.last_name}, None)
        except Exception as e:
            return _reply(f"Couldn't update: {e}", last_user, None)
    return _reply("I'm not sure I understood that. Try \"help\" to see what I can do.", last_user, None)


def _reply(text, last_user, pending):
    return {"reply": text, "context": {"last_user": last_user, "pending": pending}}