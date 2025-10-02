from flask import abort, request
from flask_login import current_user
from app import db
from models import AuditLog


def log_action(user, action, details=None):
    """Utility to log any user action into the audit log."""
    log = AuditLog(
        user_id=user.id if user and user.is_authenticated else None,
        action=action,
        details=details,
    )
    db.session.add(log)
    db.session.commit()


def require_role(*roles):
    """
    Enforce role-based access.
    Example:
        require_role("admin", "superadmin")
    """
    if not current_user.is_authenticated:
        log_action(None, "UNAUTHORIZED_ACCESS", f"Attempted access to {request.path}")
        abort(401)  # Unauthorized

    if current_user.role_obj.name not in roles:
        log_action(
            current_user,
            "FORBIDDEN_ACCESS",
            f"User {current_user.email} tried to access {request.path}",
        )
        abort(403)  # Forbidden

    return True


def is_superadmin():
    """Returns True if current user is superadmin, else logs if denied."""
    if not current_user.is_authenticated:
        log_action(None, "UNAUTHORIZED_SUPERADMIN_CHECK", "Unauthenticated check")
        return False

    if current_user.role_obj.name == "superadmin":
        return True

    log_action(
        current_user,
        "FORBIDDEN_SUPERADMIN_CHECK",
        f"User {current_user.email} attempted superadmin-only action",
    )
    return False


def is_admin():
    """Returns True if current user is admin or superadmin, else logs if denied."""
    if not current_user.is_authenticated:
        log_action(None, "UNAUTHORIZED_ADMIN_CHECK", "Unauthenticated check")
        return False

    if current_user.role_obj.name in ["admin", "superadmin"]:
        return True

    log_action(
        current_user,
        "FORBIDDEN_ADMIN_CHECK",
        f"User {current_user.email} attempted admin-only action",
    )
    return False


def is_staff():
    """Returns True if current user is staff, else logs if denied."""
    if not current_user.is_authenticated:
        log_action(None, "UNAUTHORIZED_STAFF_CHECK", "Unauthenticated check")
        return False

    if current_user.role_obj.name == "staff":
        return True

    log_action(
        current_user,
        "FORBIDDEN_STAFF_CHECK",
        f"User {current_user.email} attempted staff-only action",
    )
    return False
