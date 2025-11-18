from fastapi import FastAPI
from sqlalchemy import create_engine
from models import Base

# データベースの設定
DATABASE_URL = "sqlite:///./medication_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# テーブルを実際に作成するコマンド
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
  return {"message": "API is running!"}