from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ユーザーテーブル
class User(Base):
  __tablename__ = "users"
  user_id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password_hash = Column(String)

  # リレーション
  medications = relationship("Medication", back_populates="owner")

# 薬テーブル
class Medication(Base):
  __tablename__ = "medications"
  medication_id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.user_id"))
  name = Column(String, index=True)
  dosage = Column(String)
  is_as_needed = Column(Boolean, default=False)
  memo = Column(String, nullable=True)

  # リレーション
  owner = relationship("User", back_populates="medications")
  timings = relationship("MedicatonTiming", back_populates="medication")

# 服薬時刻テーブル
class MedicationTiming(Base):
  __tablename__ = "medication_timings"
  timing_id = Column(Integer, primary_key=True, index=True)
  medication_id = Column(Integer, ForeignKey("medications.medication_id"))
  take_time = Column(Time)

  # リレーション
  medication = relationship("Medication", back_populates="timings")

# 服薬履歴テーブル
class IntakeRecord(Base):
  __tablename__ = "intake_records"
  record_id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.user_id"))
  medication_id = Column(Integer, ForeignKey("medications.medication_id"))
  timing_id = Column(Integer, ForeignKey("medication_timings.timing_id"), nullable=True)
  taken_at = Column(DateTime)