"""Create initial Shram Saathi marketplace schema."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geography

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


account_status = postgresql.ENUM(
    "ACTIVE", "SUSPENDED", "DELETED", name="accountstatus", create_type=False
)
user_role = postgresql.ENUM(
    "WORKER", "CONTRACTOR", "CUSTOMER", "ADMIN", name="userrole", create_type=False
)
job_status = postgresql.ENUM(
    "DRAFT", "OPEN", "PAUSED", "CLOSED", "EXPIRED", name="jobstatus", create_type=False
)
wage_unit = postgresql.ENUM(
    "HOUR", "DAY", "TASK", "MONTH", "NEGOTIABLE", name="wageunit", create_type=False
)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    bind = op.get_bind()
    account_status.create(bind, checkfirst=True)
    user_role.create(bind, checkfirst=True)
    job_status.create(bind, checkfirst=True)
    wage_unit.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("phone_e164", sa.String(length=20), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("preferred_language", sa.String(length=5), nullable=False),
        sa.Column("account_status", account_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_phone_e164", "users", ["phone_e164"], unique=True)

    op.create_table(
        "user_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "role", name="uq_user_role"),
    )
    op.create_index("ix_user_roles_user_id", "user_roles", ["user_id"])

    op.create_table(
        "worker_profiles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("locality", sa.String(length=120), nullable=False),
        sa.Column("district", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("postal_code", sa.String(length=10), nullable=True),
        sa.Column("approximate_location", Geography(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("travel_radius_km", sa.Integer(), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "employer_profiles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("employer_type", sa.String(length=30), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "skill_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("name_hi", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("name_hi", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["skill_categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_skills_category_id", "skills", ["category_id"])

    op.create_table(
        "worker_skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("worker_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("skill_level", sa.String(length=30), nullable=False),
        sa.Column("experience_months", sa.Integer(), nullable=False),
        sa.Column("expected_min_amount", sa.Numeric(10, 2), nullable=True),
        sa.Column("expected_max_amount", sa.Numeric(10, 2), nullable=True),
        sa.Column("wage_unit", wage_unit, nullable=False),
        sa.ForeignKeyConstraint(["worker_id"], ["worker_profiles.user_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("worker_id", "skill_id", name="uq_worker_skill"),
    )
    op.create_index("ix_worker_skills_worker_id", "worker_skills", ["worker_id"])
    op.create_index("ix_worker_skills_skill_id", "worker_skills", ["skill_id"])

    op.create_table(
        "jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("employer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("worker_count", sa.Integer(), nullable=False),
        sa.Column("locality", sa.String(length=120), nullable=False),
        sa.Column("district", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("work_location", Geography(geometry_type="POINT", srid=4326), nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("wage_min", sa.Numeric(10, 2), nullable=True),
        sa.Column("wage_max", sa.Numeric(10, 2), nullable=True),
        sa.Column("wage_unit", wage_unit, nullable=False),
        sa.Column("status", job_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["employer_id"], ["employer_profiles.user_id"]),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_jobs_employer_id", "jobs", ["employer_id"])
    op.create_index("ix_jobs_skill_id", "jobs", ["skill_id"])
    op.create_index("ix_jobs_status", "jobs", ["status"])

    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("worker_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("proposed_amount", sa.Numeric(10, 2), nullable=True),
        sa.Column("wage_unit", wage_unit, nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["worker_id"], ["worker_profiles.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id", "worker_id", name="uq_job_worker_application"),
    )
    op.create_index("ix_applications_job_id", "applications", ["job_id"])
    op.create_index("ix_applications_worker_id", "applications", ["worker_id"])


def downgrade() -> None:
    op.drop_index("ix_applications_worker_id", table_name="applications")
    op.drop_index("ix_applications_job_id", table_name="applications")
    op.drop_table("applications")
    op.drop_index("ix_jobs_status", table_name="jobs")
    op.drop_index("ix_jobs_skill_id", table_name="jobs")
    op.drop_index("ix_jobs_employer_id", table_name="jobs")
    op.drop_table("jobs")
    op.drop_index("ix_worker_skills_skill_id", table_name="worker_skills")
    op.drop_index("ix_worker_skills_worker_id", table_name="worker_skills")
    op.drop_table("worker_skills")
    op.drop_index("ix_skills_category_id", table_name="skills")
    op.drop_table("skills")
    op.drop_table("skill_categories")
    op.drop_table("employer_profiles")
    op.drop_table("worker_profiles")
    op.drop_index("ix_user_roles_user_id", table_name="user_roles")
    op.drop_table("user_roles")
    op.drop_index("ix_users_phone_e164", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    wage_unit.drop(bind, checkfirst=True)
    job_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
    account_status.drop(bind, checkfirst=True)
