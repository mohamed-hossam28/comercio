import secrets
from typing import Optional

# Simple in-memory session store: token -> user_id
_sessions: dict[str, int] = {}


def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[token] = user_id
    return token


def get_user_id_from_token(token: Optional[str]) -> Optional[int]:
    if not token:
        return None
    return _sessions.get(token)


def invalidate_session(token: str) -> None:
    _sessions.pop(token, None)
