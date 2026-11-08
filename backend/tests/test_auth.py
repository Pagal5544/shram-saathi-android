from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core import auth
from app.core.config import settings
from app.core.database import get_db
from app.main import app

client = TestClient(app)


def test_firebase_exchange_rejects_invalid_token(monkeypatch):
    def reject(_token):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Firebase ID token is invalid or expired")

    monkeypatch.setattr(auth, "verify_firebase_phone_token", reject)
    response = client.post("/api/v1/auth/firebase", json={"id_token": "x" * 40})
    assert response.status_code == 401


def test_access_token_contains_expected_claims(monkeypatch):
    monkeypatch.setattr(settings, "jwt_secret_key", "x" * 40)
    user_id = uuid4()
    token, expires_in = auth.create_access_token(user_id)
    claims = jwt.decode(
        token,
        "x" * 40,
        algorithms=["HS256"],
        issuer="shram-saathi-api",
    )
    assert claims["sub"] == str(user_id)
    assert claims["type"] == "access"
    assert expires_in == settings.access_token_minutes * 60


def test_worker_registration_requires_authentication():
    response = client.post("/api/v1/profiles/worker", json={
        "display_name": "Test Worker",
        "locality": "Meerut",
        "skill_ids": [],
    })
    assert response.status_code == 401


def test_employer_registration_requires_authentication():
    response = client.post("/api/v1/profiles/employer", json={
        "display_name": "Test Contractor",
    })
    assert response.status_code == 401
