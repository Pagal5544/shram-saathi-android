"""Firebase identity verification and short-lived API access tokens."""
import json
import threading
from datetime import datetime, timedelta, timezone
from uuid import UUID

import firebase_admin
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth, credentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import AccountStatus, User

_bearer = HTTPBearer(auto_error=False)
_firebase_lock = threading.Lock()


def _firebase_app():
    if firebase_admin._apps:
        return firebase_admin.get_app()
    with _firebase_lock:
        if firebase_admin._apps:
            return firebase_admin.get_app()
        raw = settings.firebase_service_account_json
        if not raw:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Firebase authentication is not configured",
            )
        try:
            service_account = json.loads(raw)
            return firebase_admin.initialize_app(credentials.Certificate(service_account))
        except (ValueError, TypeError, KeyError) as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Firebase authentication configuration is invalid",
            ) from exc


def verify_firebase_phone_token(id_token: str) -> tuple[str, str]:
    """Return Firebase UID and its phone number, which Firebase assigns after verification."""
    _firebase_app()
    try:
        decoded = firebase_auth.verify_id_token(id_token, check_revoked=True)
        firebase_user = firebase_auth.get_user(decoded["uid"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase ID token is invalid or expired",
        ) from exc

    phone = firebase_user.phone_number
    if not phone:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A verified phone number is required",
        )
    return firebase_user.uid, phone


def create_access_token(user_id: UUID) -> tuple[str, int]:
    secret = settings.jwt_secret_key
    if len(secret) < 32:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API token signing is not configured securely",
        )
    expires_in = settings.access_token_minutes * 60
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(seconds=expires_in),
            "iss": "shram-saathi-api",
            "type": "access",
        },
        secret,
        algorithm="HS256",
    )
    return token, expires_in


def get_current_user(
    credentials_: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if credentials_ is None or credentials_.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer access token required")
    if len(settings.jwt_secret_key) < 32:
        raise HTTPException(status_code=503, detail="API token signing is not configured")
    try:
        payload = jwt.decode(
            credentials_.credentials,
            settings.jwt_secret_key,
            algorithms=["HS256"],
            issuer="shram-saathi-api",
            options={"require": ["sub", "exp", "iat", "iss", "type"]},
        )
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Wrong token type")
        user_id = UUID(payload["sub"])
    except (jwt.InvalidTokenError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired access token") from exc

    user = db.get(User, user_id)
    if user is None or user.account_status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=401, detail="Account is unavailable")
    return user
