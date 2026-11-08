from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SkillPublic(BaseModel):
    id: UUID
    category_id: UUID
    category_name: str
    category_name_hi: str | None = None
    name: str
    name_hi: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobPublic(BaseModel):
    id: UUID
    title: str
    description: str
    skill_id: UUID
    skill_name: str
    skill_name_hi: str | None = None
    worker_count: int
    locality: str
    district: str | None = None
    state: str
    start_date: datetime | None = None
    wage_min: Decimal | None = None
    wage_max: Decimal | None = None
    wage_unit: str
    created_at: datetime
    employer_name: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedJobs(BaseModel):
    items: list[JobPublic]
    total: int
    limit: int
    offset: int
