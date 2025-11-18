from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from typing import List

import crud, models, schemas

# DB設定
DATABASE_URL = "sqlite:///./medication_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テーブル作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
  "http://localhost:5173",
]

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