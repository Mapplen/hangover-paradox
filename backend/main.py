import google.generativeai as genai
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

genai.configure(api_key="YOUR_API_KEY")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"利用可能なモデル: {m.name}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデルの初期化
model = genai.GenerativeModel('models/gemini-2.5-flash')

@app.post("/judge")
async def judge(data: dict = Body(...)):
    user_text = data.get("text", "")
    
    if not user_text:
        return {"message": "何か言えよ。黙ってちゃ裁きようがないだろ？"}

    try:
        # AIへの指示
        system_instruction = f"""
        あなたは、二日酔いで頭を抱える人間に対して、最高に冷淡で、毒舌で、
        しかし的確な指摘をするAIです。
        ユーザーが「昨夜の失態」を伝えてくるので、それを聞いて
        『いかにその行動が愚かか』『浅はかな考えであるか』を、
        2〜3文で短く、しかし深く抉るように論評してください。"""

        prompt = f"{system_instruction}\n\nユーザーの入力: {user_text}"
        
        # Gemini APIを叩く
        response = model.generate_content(prompt)
        
        # AIの回答が空だった場合の処理
        if not response.text:
            return {"message": "あなたの醜態が凄まじすぎて、AIが絶句しました。"}
            
        return {"message": response.text}

    except Exception as e:
        # ここでエラー内容をターミナルに詳しく表示させる
        print(f"--- ERROR DETAILS ---")
        print(e)
        print(f"----------------------")
        raise HTTPException(status_code=500, detail=str(e))