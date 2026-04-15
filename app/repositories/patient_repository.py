"""Repository for patient records."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate


def create_patient(db: Session, data: PatientCreate) -> Patient:
    model = Patient(name=data.name, email=data.email)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def get_patient_by_id(db: Session, patient_id: str) -> Optional[Patient]:
    stmt = select(Patient).where(Patient.id == patient_id)
    return db.execute(stmt).scalar_one_or_none()


def get_patient_by_email(db: Session, email: str) -> Optional[Patient]:
    stmt = select(Patient).where(Patient.email == email)
    return db.execute(stmt).scalar_one_or_none()
