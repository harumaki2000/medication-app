from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from typing import List
from datetime import timedelta

import crud, models, schemas, auth

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