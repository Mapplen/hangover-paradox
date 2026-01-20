from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ここで「3000番（フロントエンド）」からの通信を許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "ようやく通信が繋がりましたね。これであなたの醜態を記録する準備が整いました。",
        "next_step": "画面の文字が変わったなら、フロントとバックの『握手』成功です。"
    }