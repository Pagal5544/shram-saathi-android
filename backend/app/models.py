import enum
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geography
from app.core.database import Base


class AccountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class UserRole(str, enum.Enum):
    WORKER = "WORKER"
    CONTRACTOR = "CONTRACTOR"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


class JobStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"


class WageUnit(str, enum.Enum):
    HOUR = "HOUR"
    DAY = "DAY"
    TASK = "TASK"
    MONTH = "MONTH"
    NEGOTIABLE = "NEGOTIABLE"


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_e164: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(100))
    preferred_language: Mapped[str] = mapped_column(String(5), default="hi")
    account_status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserRoleRecord(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role", name="uq_user_role"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))


class WorkerProfile(Base):
    __tablename__ = "worker_profiles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    locality: Mapped[str] = mapped_column(String(120))
    district: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str] = mapped_column(String(120), default="Uttar Pradesh")
    postal_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    approximate_location = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    travel_radius_km: Mapped[int] = mapped_column(Integer, default=10)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)


class EmployerProfile(Base):
    __tablename__ = "employer_profiles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    employer_type: Mapped[str] = mapped_column(String(30), default="INDIVIDUAL")
    display_name: Mapped[str] = mapped_column(String(120))


class SkillCategory(Base):
    __tablename__ = "skill_categories"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    name_hi: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skill_categories.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    name_hi: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class WorkerSkill(Base):
    __tablename__ = "worker_skills"
    __table_args__ = (UniqueConstraint("worker_id", "skill_id", name="uq_worker_skill"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("worker_profiles.user_id", ondelete="CASCADE"), index=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), index=True)
    skill_level: Mapped[str] = mapped_column(String(30), default="SEMI_SKILLED")
    experience_months: Mapped[int] = mapped_column(Integer, default=0)
    expected_min_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    expected_max_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    wage_unit: Mapped[WageUnit] = mapped_column(Enum(WageUnit), default=WageUnit.DAY)


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employer_profiles.user_id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text, default="")
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"), index=True)
    worker_count: Mapped[int] = mapped_column(Integer, default=1)
    locality: Mapped[str] = mapped_column(String(120))
    district: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str] = mapped_column(String(120), default="Uttar Pradesh")
    work_location = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    wage_min: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    wage_max: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    wage_unit: Mapped[WageUnit] = mapped_column(Enum(WageUnit), default=WageUnit.DAY)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.DRAFT, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("job_id", "worker_id", name="uq_job_worker_application"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    worker_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("worker_profiles.user_id", ondelete="CASCADE"), index=True)
    proposed_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    wage_unit: Mapped[WageUnit] = mapped_column(Enum(WageUnit), default=WageUnit.DAY)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(24), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
