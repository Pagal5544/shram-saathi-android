from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app

client = TestClient(app)


class EmptyResult:
    def all(self):
        return []

    def first(self):
        return None


class FakeSession:
    def execute(self, statement):
        return EmptyResult()

    def scalar(self, statement):
        return 0


def override_db():
    yield FakeSession()


app.dependency_overrides[get_db] = override_db


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Shram Saathi API"


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_skills_endpoint_returns_empty_list():
    response = client.get("/api/v1/skills")
    assert response.status_code == 200
    assert response.json() == []


def test_jobs_endpoint_returns_paginated_empty_result():
    response = client.get("/api/v1/jobs")
    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "limit": 20,
        "offset": 0,
    }


def test_job_detail_returns_404_when_missing():
    response = client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 404
