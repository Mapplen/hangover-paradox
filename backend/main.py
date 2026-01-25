import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"現在使用可能なモデル名: {m.name}")

# --- データベース設定 ---
DATABASE_URL = "sqlite:///./confessions.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 標本（レコード）の定義
class ConfessionRecord(Base):
    __tablename__ = "confessions"
    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(Text)
    censure = Column(Text)
    remedy = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

# テーブル作成
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定（既存のまま）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = genai.GenerativeModel('models/gemini-2.5-flash')

@app.post("/judge")
async def judge(data: dict = Body(...)):
    user_text = data.get("text", "")
    if not user_text:
        raise HTTPException(status_code=400, detail="無言の告白は受け付けない。")

    try:
        system_instruction = (        
            "あなたは冷徹な教誨師です。懺悔を聞き、以下の2点のみを出力してください。\n\n"
            "【断罪】ユーザーの行動に潜む浅ましさや愚かさを、鋭い一言で指摘してください。\n\n"
            "【救済】その醜態を二度と繰り返さないための、具体的かつ事務的な解決策を1文で提示してください。\n\n"
            "共感や慰めは一切不要です。あくまで淡々と本質的な指摘を、深くえぐるように。")
        
        prompt = f"{system_instruction}\n\nユーザーの入力: {user_text}"
        response = model.generate_content(prompt)
        full_text = response.text

        # 簡易パース
        censure = full_text.split("【救済】")[0].replace("【断罪】", "").strip()
        remedy = full_text.split("【救済】")[1].strip() if "【救済】" in full_text else ""

        # --- データベースに保存 ---
        db = SessionLocal()
        new_record = ConfessionRecord(
            user_text=user_text,
            censure=censure,
            remedy=remedy
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        db.close()

        return {"message": full_text}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 過去の標本を取得するエンドポイント（後でフロントから使う）
@app.get("/history")
async def get_history():
    db = SessionLocal()
    records = db.query(ConfessionRecord).order_by(ConfessionRecord.created_at.desc()).all()
    db.close()
    return records