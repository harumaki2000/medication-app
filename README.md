## 服薬管理Webアプリ   
 
毎日の服薬スケジュールを管理し、飲み忘れを防止するための服薬管理Webアプリケーションです。  
現在開発中です。  
 
### 概要  
服薬管理が複雑になると薬を飲んだかどうかわからなくなったり、管理ができず飲み忘れが起こったりすることが多いと感じたので  
簡単に服薬管理ができる・分かりやすくなるを目指して開発しています。  
 
### 使用技術  
#### Backend  
- Language: Python 3.13
- Framework: FastAPI
- ORM: SQLAlchemy
- Schema Validation: Pydantic V2
- Database: SQLite (開発環境)

#### Frontend
- Language: TypeScript
- Framework: Vue.js 3
- Build Tool: Vite
- HTTP Client: Axios
- Styling: CSS Modules / Scoped CSS

### 機能  
#### 実装済み  
- ユーザー管理
  - 新規ユーザー登録 (Frontend & Backend)
  - パスワードの確認入力チェック (Frontend)
- 薬の管理(APIのみ実装済み)
  - 薬の登録 (名称、服用量、頓服フラグ、メモ)
  - 服薬時刻の登録 (1つの薬に対して複数の時間を紐づけ可能)
  - 薬の一覧取得
- データベース設計
  - ユーザー、薬、服薬時刻、服薬履歴の正規化されたテーブル設計
 
#### 今後実装予定
- ログイン / ログアウト機能 (JWT認証)
- 薬の登録・編集・削除画面 (CRUD UI)
- 本日の服薬タスク表示ダッシュボード  
- 服薬チェック(記録)機能  
- Dockerによるコンテナ化

### 開発環境のセットアップ (Linux環境想定)
#### Backend (Python / FastAPI)
```
cd backend
python -m venv venv

source venv/bin/activate

pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload
```
 
#### Frontend (Vue.js / TypeScript)
```
cd frontend
npm install
npm run dev
```