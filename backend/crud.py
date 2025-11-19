from sqlalchemy.orm import Session
from datetime import datetime, date, time
from typing import Optional
import models, schemas, auth

# Create User
def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = auth.get_password_hash(user.password)

  db_user = models.User(
    email = user.email,
    username = user.username,
    password_hash = hashed_password
  )

  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

# Read Medications
def get_medications(db: Session, user_id: int):
  return db.query(models.Medication).filter(models.Medication.user_id == user_id).all()

# Create Medication
def create_medication(db: Session, medication: schemas.MedicationCreate, user_id: int):
  db_medication = models.Medication(
    name = medication.name,
    dosage = medication.dosage,
    is_as_needed = medication.is_as_needed,
    memo = medication.memo,
    user_id = user_id
  )

  db.add(db_medication)
  db.commit()
  db.refresh(db_medication)

  for t in medication.timings:
    db_timing = models.MedicationTiming(
      take_time = t,
      medication_id = db_medication.medication_id
    )
    db.add(db_timing)

  db.commit()

  db.refresh(db_medication)
  return db_medication

def create_intake_record(db: Session, record: schemas.IntakeRecordCreate, user_id: int):
  taken_time = record.taken_at or datetime.utcnow()

  db_record = models.IntakeRecord(
    user_id = user_id,
    medication_id = record.medication_id,
    timing_id = record.timing_id,
    taken_at = taken_time
  )

  db.add(db_record)
  db.commit()
  db.refresh(db_record)
  return db_record

def get_intake_records(db: Session, user_id: int, target_date: Optional[date] = None):
  query = db.query(models.IntakeRecord).filter(models.IntakeRecord.user_id == user_id)

  if target_date:
    start = datetime.combine(target_date, time.min)
    end = datetime.combine(target_date, time.max)
    query = query.filter(models.IntakeRecord.taken_at >= start, models.IntakeRecord.taken_at <= end)

  return query.all()

def get_today_intake_records(db: Session, user_id: int):
  today = date.today()
  return get_intake_records(db=db, user_id=user_id, target_date=today)

def delete_medication(db: Session, medication_id: int, user_id: int):
  medication = db.query(models.Medication).filter(
    models.Medication.medication_id == medication_id,
    models.Medication.user_id == user_id
  ).first()

  if not medication:
    return False

  db.query(models.IntakeRecord).filter(models.IntakeRecord.medication_id == medication_id).delete()
  db.query(models.MedicationTiming).filter(models.MedicationTiming.medication_id == medication_id).delete()
  db.delete(medication)
  db.commit()
  return True

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()
