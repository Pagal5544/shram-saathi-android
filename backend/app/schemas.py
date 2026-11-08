from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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


class AuthExchangeRequest(BaseModel):
    id_token: str = Field(min_length=20, max_length=8192)


class AuthSessionResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: UUID
    phone_e164: str
    roles: list[str]


class WorkerRegistration(BaseModel):
    display_name: str = Field(min_length=2, max_length=100)
    bio: str | None = Field(default=None, max_length=1000)
    locality: str = Field(min_length=2, max_length=120)
    district: str | None = Field(default=None, max_length=120)
    state: str = Field(default="Uttar Pradesh", min_length=2, max_length=120)
    postal_code: str | None = Field(default=None, pattern=r"^\d{6}$")
    travel_radius_km: int = Field(default=10, ge=1, le=100)
    is_available: bool = True
    skill_ids: list[UUID] = Field(default_factory=list, max_length=30)
    skill_level: Literal["UNSKILLED", "SEMI_SKILLED", "SKILLED", "EXPERT"] = "SEMI_SKILLED"
    experience_months: int = Field(default=0, ge=0, le=720)
    expected_min_amount: Decimal | None = Field(default=None, ge=0, le=10000000)
    expected_max_amount: Decimal | None = Field(default=None, ge=0, le=10000000)
    wage_unit: Literal["HOUR", "DAY", "TASK", "MONTH", "NEGOTIABLE"] = "DAY"


class EmployerRegistration(BaseModel):
    display_name: str = Field(min_length=2, max_length=120)
    employer_type: Literal["INDIVIDUAL", "CONTRACTOR", "COMPANY"] = "INDIVIDUAL"
    role: Literal["CONTRACTOR", "CUSTOMER"] = "CONTRACTOR"


class ProfileResponse(BaseModel):
    user_id: UUID
    display_name: str
    roles: list[str]
