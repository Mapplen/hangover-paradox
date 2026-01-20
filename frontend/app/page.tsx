"use client";
import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("ここに皮肉が表示されます");

  const fetchIrony = async () => {
    try {
      // バックエンド（FastAPI）にデータをとりに行く
      const response = await fetch("http://127.0.0.1:8000/");
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      setMessage("バックエンドが寝てます。uvicornは動いてますか？");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-black text-white">
      <h1 className="text-4xl font-bold mb-8 text-red-600">Hangover Paradox</h1>
      <div className="p-6 border border-gray-700 rounded-lg bg-gray-900">
        <p className="text-xl italic mb-4">"{message}"</p>
        <button
          onClick={fetchIrony}
          className="px-4 py-2 bg-red-700 hover:bg-red-500 rounded font-bold transition-colors"
        >
          昨夜の自分を呼び出す
        </button>
      </div>
    </main>
  );
}