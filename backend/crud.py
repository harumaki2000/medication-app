from sqlalchemy.orm import Session
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

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()