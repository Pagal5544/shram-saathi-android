"""Phone identity exchange and authenticated profile registration."""
import re
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, get_current_user, verify_firebase_phone_token
from app.core.config import settings
from app.core.database import get_db
from app.models import (
    EmployerProfile,
    Skill,
    User,
    UserRole,
    UserRoleRecord,
    WageUnit,
    WorkerProfile,
    WorkerSkill,
)
from app.schemas import (
    AuthExchangeRequest,
    AuthSessionResponse,
    EmployerRegistration,
    ProfileResponse,
    WorkerRegistration,
)

router = APIRouter(prefix=f"{settings.api_v1_prefix}/auth", tags=["authentication"])
profile_router = APIRouter(prefix=f"{settings.api_v1_prefix}/profiles", tags=["profiles"])
_PHONE_RE = re.compile(r"^\+[1-9]\d{7,14}$")


def _roles(db: Session, user_id: UUID) -> list[str]:
    return list(db.scalars(select(UserRoleRecord.role).where(UserRoleRecord.user_id == user_id)))


@router.post("/firebase", response_model=AuthSessionResponse)
def exchange_firebase_token(payload: AuthExchangeRequest, db: Session = Depends(get_db)):
    _, phone = verify_firebase_phone_token(payload.id_token)
    if not _PHONE_RE.fullmatch(phone):
        raise HTTPException(status_code=400, detail="Firebase returned an invalid phone number")

    user = db.scalar(select(User).where(User.phone_e164 == phone))
    if user is None:
        user = User(phone_e164=phone, display_name="New User", preferred_language="hi")
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            user = db.scalar(select(User).where(User.phone_e164 == phone))
            if user is None:
                raise
        else:
            db.refresh(user)

    if user.account_status.value != "ACTIVE":
        raise HTTPException(status_code=403, detail="This account is not active")

    token, expires_in = create_access_token(user.id)
    return AuthSessionResponse(
        access_token=token,
        expires_in=expires_in,
        user_id=user.id,
        phone_e164=user.phone_e164,
        roles=_roles(db, user.id),
    )


@profile_router.post("/worker", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def register_worker(
    payload: WorkerRegistration,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.expected_min_amount is not None and payload.expected_max_amount is not None:
        if payload.expected_min_amount > payload.expected_max_amount:
            raise HTTPException(status_code=422, detail="Minimum wage cannot exceed maximum wage")

    if len(payload.skill_ids) != len(set(payload.skill_ids)):
        raise HTTPException(status_code=422, detail="Duplicate skill IDs are not allowed")
    skills = list(db.scalars(select(Skill).where(
        Skill.id.in_(payload.skill_ids), Skill.is_active.is_(True)
    )))
    if len(skills) != len(set(payload.skill_ids)):
        raise HTTPException(status_code=422, detail="One or more skills are invalid or inactive")

    profile = db.get(WorkerProfile, current_user.id)
    if profile is None:
        profile = WorkerProfile(user_id=current_user.id, locality=payload.locality)
        db.add(profile)
    profile.bio = payload.bio
    profile.locality = payload.locality
    profile.district = payload.district
    profile.state = payload.state
    profile.postal_code = payload.postal_code
    profile.travel_radius_km = payload.travel_radius_km
    profile.is_available = payload.is_available
    current_user.display_name = payload.display_name

    existing = list(db.scalars(select(WorkerSkill).where(WorkerSkill.worker_id == current_user.id)))
    for item in existing:
        db.delete(item)
    for skill_id in payload.skill_ids:
        db.add(WorkerSkill(
            worker_id=current_user.id,
            skill_id=skill_id,
            skill_level=payload.skill_level,
            experience_months=payload.experience_months,
            expected_min_amount=payload.expected_min_amount,
            expected_max_amount=payload.expected_max_amount,
            wage_unit=WageUnit(payload.wage_unit),
        ))
    role = db.scalar(select(UserRoleRecord).where(
        UserRoleRecord.user_id == current_user.id,
        UserRoleRecord.role == UserRole.WORKER,
    ))
    if role is None:
        db.add(UserRoleRecord(user_id=current_user.id, role=UserRole.WORKER))
    db.commit()
    return ProfileResponse(user_id=current_user.id, display_name=current_user.display_name, roles=_roles(db, current_user.id))


@profile_router.post("/employer", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def register_employer(
    payload: EmployerRegistration,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.get(EmployerProfile, current_user.id)
    if profile is None:
        profile = EmployerProfile(user_id=current_user.id, display_name=payload.display_name)
        db.add(profile)
    profile.display_name = payload.display_name
    profile.employer_type = payload.employer_type
    current_user.display_name = payload.display_name

    role = db.scalar(select(UserRoleRecord).where(
        UserRoleRecord.user_id == current_user.id,
        UserRoleRecord.role == payload.role,
    ))
    if role is None:
        db.add(UserRoleRecord(user_id=current_user.id, role=payload.role))
    db.commit()
    return ProfileResponse(user_id=current_user.id, display_name=current_user.display_name, roles=_roles(db, current_user.id))
