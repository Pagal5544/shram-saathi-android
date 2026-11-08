from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import EmployerProfile, Job, JobStatus, Skill, SkillCategory
from app.schemas import JobPublic, PaginatedJobs, SkillPublic

router = APIRouter(prefix=settings.api_v1_prefix, tags=["marketplace"])


@router.get("/skills", response_model=list[SkillPublic])
def list_skills(
    category_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    statement = (
        select(Skill, SkillCategory)
        .join(SkillCategory, Skill.category_id == SkillCategory.id)
        .where(Skill.is_active.is_(True), SkillCategory.is_active.is_(True))
        .order_by(SkillCategory.name, Skill.name)
    )
    if category_id is not None:
        statement = statement.where(Skill.category_id == category_id)

    rows = db.execute(statement).all()
    return [
        SkillPublic(
            id=skill.id,
            category_id=category.id,
            category_name=category.name,
            category_name_hi=category.name_hi,
            name=skill.name,
            name_hi=skill.name_hi,
        )
        for skill, category in rows
    ]


def _job_public(job: Job, skill: Skill, employer: EmployerProfile) -> JobPublic:
    return JobPublic(
        id=job.id,
        title=job.title,
        description=job.description,
        skill_id=skill.id,
        skill_name=skill.name,
        skill_name_hi=skill.name_hi,
        worker_count=job.worker_count,
        locality=job.locality,
        district=job.district,
        state=job.state,
        start_date=job.start_date,
        wage_min=job.wage_min,
        wage_max=job.wage_max,
        wage_unit=job.wage_unit.value,
        created_at=job.created_at,
        employer_name=employer.display_name,
    )


@router.get("/jobs", response_model=PaginatedJobs)
def list_open_jobs(
    district: str | None = Query(default=None, min_length=2, max_length=120),
    skill_id: UUID | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    filters = [Job.status == JobStatus.OPEN]
    if district:
        filters.append(func.lower(Job.district) == district.strip().lower())
    if skill_id:
        filters.append(Job.skill_id == skill_id)

    total = db.scalar(select(func.count(Job.id)).where(*filters)) or 0
    statement = (
        select(Job, Skill, EmployerProfile)
        .join(Skill, Job.skill_id == Skill.id)
        .join(EmployerProfile, Job.employer_id == EmployerProfile.user_id)
        .where(*filters)
        .order_by(Job.created_at.desc(), Job.id)
        .limit(limit)
        .offset(offset)
    )
    rows = db.execute(statement).all()
    return PaginatedJobs(
        items=[_job_public(job, skill, employer) for job, skill, employer in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/jobs/{job_id}", response_model=JobPublic)
def get_open_job(job_id: UUID, db: Session = Depends(get_db)):
    statement = (
        select(Job, Skill, EmployerProfile)
        .join(Skill, Job.skill_id == Skill.id)
        .join(EmployerProfile, Job.employer_id == EmployerProfile.user_id)
        .where(Job.id == job_id, Job.status == JobStatus.OPEN)
    )
    row = db.execute(statement).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Open job not found")
    return _job_public(*row)
