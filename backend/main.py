import os
from datetime import timedelta, datetime
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import auth
import crud
import models
import schemas

load_dotenv()

# DB設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medication_app.db")
engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テーブル作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins_env = os.getenv("ALLOWED_ORIGINS")
default_origins = [
  "http://localhost",
  "http://localhost:80",
  "http://localhost:5173",
  "http://127.0.0.1",
  "http://127.0.0.1:8000",
]
origins = [
  origin.strip() for origin in origins_env.split(",")
  if origin.strip()
] if origins_env else default_origins

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# ユーザー登録api
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  return crud.create_user(db=db, user=user)

# 薬の登録api
@app.post("/users/{user_id}/medications/", response_model=schemas.Medication)
def create_medication_for_user(
  user_id: int,
  medication: schemas.MedicationCreate,
  db: Session = Depends(get_db)
):
  return crud.create_medication(db=db, medication=medication, user_id=user_id)

# 薬の一覧取得api
@app.get("/users/{user_id}/medications/", response_model=List[schemas.Medication])
def read_medications(user_id: int, db: Session = Depends(get_db)):
  medications = crud.get_medications(db=db, user_id=user_id)
  return medications

@app.post("/users/{user_id}/intake-records/", response_model=schemas.IntakeRecord)
def create_intake_record_for_user(
  user_id: int,
  intake: schemas.IntakeRecordCreate,
  db: Session = Depends(get_db)
):
  medication = db.query(models.Medication).filter(
    models.Medication.medication_id == intake.medication_id,
    models.Medication.user_id == user_id
  ).first()

  if not medication:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="指定した薬が見つかりません"
    )

  return crud.create_intake_record(db=db, record=intake, user_id=user_id)


@app.get("/users/{user_id}/intake-records/", response_model=List[schemas.IntakeRecord])
def list_intake_records(
  user_id: int,
  date: Optional[str] = None,
  db: Session = Depends(get_db)
):
  target_date = None
  if date:
    try:
      target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="日付は YYYY-MM-DD 形式で指定してください"
      )

  records = crud.get_intake_records(
    db=db,
    user_id=user_id,
    target_date=target_date or datetime.utcnow().date()
  )
  return records


@app.get("/users/{user_id}/records/today", response_model=List[schemas.IntakeRecord])
def list_today_records(user_id: int, db: Session = Depends(get_db)):
  return crud.get_today_intake_records(db=db, user_id=user_id)


@app.delete("/users/{user_id}/medications/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(user_id: int, medication_id: int, db: Session = Depends(get_db)):
  success = crud.delete_medication(db=db, medication_id=medication_id, user_id=user_id)

  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="指定した薬が見つかりません"
    )


@app.options("/users/")
def users_options():
  return Response(status_code=status.HTTP_204_NO_CONTENT)

# ログインAPI
@app.post("/token", response_model=dict)
def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
):
  
  user = crud.get_user_by_email(db, email=form_data.username)

  if not user or not auth.verify_password(form_data.password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="メールアドレスまたはパスワードが間違っています",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)

  access_token = auth.create_access_token(
    data={"sub": user.email}, expires_delta=access_token_expires
  )

  return {"access_token": access_token, "token_type": "bearer", "user_id": user.user_id}
