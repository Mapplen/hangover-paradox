from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/judge")
def judge(data: dict = Body(...)):
    text = data.get("text", "")
    return {"message": f"『{text}』ですって？ 昨夜のあなたは随分と饒舌だったようですね。"}