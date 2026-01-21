"use client";
import { useState } from "react";

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [response, setResponse] = useState("昨夜の醜態を入力してください。");
  const [loading, setLoading] = useState(false);

  const sendToBackend = async () => {
    if (!inputText) return;
    setLoading(true);
    try {
      // バックエンドの /judge エンドポイントを叩く
      const res = await fetch("http://127.0.0.1:8000/judge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      setResponse("バックエンドが寝ています。あるいはあなたの言葉が酷すぎて拒絶されました。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-black text-white p-6">
      <div className="w-full max-w-lg border-2 border-red-900 p-8 rounded-xl bg-gray-900 shadow-2xl">
        <h1 className="text-3xl font-black mb-6 text-red-600 tracking-tighter">
          HANGOVER PARADOX
        </h1>
        
        <textarea
          className="w-full h-32 p-4 bg-black border border-gray-700 rounded-md mb-4 text-green-400 font-mono focus:outline-none focus:border-red-500"
          placeholder="「昨夜、実はアイツのことがさぁ…」"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />

        <button
          onClick={sendToBackend}
          disabled={loading}
          className="w-full py-4 bg-red-800 hover:bg-red-600 text-white font-bold rounded-md transition-all active:scale-95 disabled:opacity-50"
        >
          {loading ? "ジャッジ中..." : "罪を報告する"}
        </button>

        <div className="mt-8 p-4 border-l-4 border-red-600 bg-black">
          <p className="text-lg italic text-gray-300">
            {response}
          </p>
        </div>
      </div>
    </main>
  );
}