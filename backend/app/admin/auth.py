from __future__ import annotations

import hashlib
import hmac
import secrets
import time

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import settings

security = HTTPBasic(auto_error=False)
SESSION_TTL_SECONDS = 12 * 60 * 60


def admin_configured() -> bool:
    if settings.ADMIN_TOKEN:
        return True
    return bool(settings.ADMIN_USERNAME and settings.ADMIN_PASSWORD)


def _session_secret() -> str:
    return settings.ADMIN_TOKEN or settings.ADMIN_PASSWORD


def issue_session() -> str:
    """Short-lived session. The raw ADMIN_TOKEN is not returned."""
    expires = int(time.time()) + SESSION_TTL_SECONDS
    message = str(expires).encode()
    signature = hmac.new(_session_secret().encode(), message, hashlib.sha256).hexdigest()
    return f"{expires}.{signature}"


def session_is_valid(value: str) -> bool:
    secret = _session_secret()
    if not secret or "." not in value:
        return False
    expires_text, signature = value.split(".", 1)
    try:
        expires = int(expires_text)
    except ValueError:
        return False
    if expires < int(time.time()):
        return False
    expected = hmac.new(secret.encode(), expires_text.encode(), hashlib.sha256).hexdigest()
    return secrets.compare_digest(expected, signature)


def _matches(left: str, right: str) -> bool:
    if not left or not right:
        return False
    return secrets.compare_digest(left, right)


def credentials_are_valid(token: str | None, username: str | None, password: str | None) -> bool:
    if token and _matches(token, settings.ADMIN_TOKEN):
        return True
    if (
        username
        and password
        and _matches(username, settings.ADMIN_USERNAME)
        and _matches(password, settings.ADMIN_PASSWORD)
    ):
        return True
    return False


def _unauthorized() -> HTTPException:
    headers = {}
    if settings.ADMIN_USERNAME and settings.ADMIN_PASSWORD:
        headers["WWW-Authenticate"] = 'Basic realm="Nawa Admin"'
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers=headers,
    )


def require_admin(
    request: Request,
    credentials: HTTPBasicCredentials | None = Depends(security),
) -> str:
    """
    Accept a bearer session, the raw ADMIN_TOKEN, or HTTP Basic username/password.
    If nothing is configured, the dashboard stays disabled.
    """
    if not admin_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin dashboard is not configured (set ADMIN_TOKEN, or ADMIN_USERNAME and ADMIN_PASSWORD)",
        )

    header = request.headers.get("authorization", "")
    if header.lower().startswith("bearer "):
        presented = header.split(" ", 1)[1].strip()
        if _matches(presented, settings.ADMIN_TOKEN) or session_is_valid(presented):
            return "admin"
        raise _unauthorized()

    if credentials and _matches(credentials.username, settings.ADMIN_USERNAME) and _matches(
        credentials.password, settings.ADMIN_PASSWORD
    ):
        return credentials.username

    raise _unauthorized()
