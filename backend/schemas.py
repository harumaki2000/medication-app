from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime

# 服薬時刻のスキーマ

class MedicationTimingBase(BaseModel):
  take_time: time

class MedicationTimingCreate(MedicationTimingBase):
  pass

class MedicationTiming(MedicationTimingBase):
  timing_id: int
  medication_id: int

  class Config:
    from_attributes = True

# Medicationのスキーマ
class MedicationBase(BaseModel):
  name: str
  dosage: str
  is_as_needed: bool = False
  memo: Optional[str] = None

class MedicationCreate(MedicationBase):
  timings: List[time]

class Medication(MedicationBase):
  medication_id: int
  user_id: int
  timings: List[MedicationTiming] = []

  class Config:
    from_attributes = True

class IntakeRecordBase(BaseModel):
  medication_id: int
  timing_id: Optional[int] = None
  taken_at: Optional[datetime] = None

class IntakeRecordCreate(IntakeRecordBase):
  pass

class IntakeRecord(IntakeRecordBase):
  record_id: int
  user_id: int

  class Config:
    from_attributes = True

# ユーザーのスキーマ
class UserBase(BaseModel):
  email: str
  username: str

class UserCreate(UserBase):
  password: str

class User(UserBase):
  user_id: int

  class Config:
    from_attributes = True
