"use client";
import { useState } from "react";

export default function Confessional() {
  const [confession, setConfession] = useState("");
  const [judgement, setJudgement] = useState({ censure: "", remedy: "" });
  const [loading, setLoading] = useState(false);

  const submitConfession = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/judge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: confession }),
      });
      const data = await res.json();
      
      // AIの返答を【断罪】と【救済】に分割して表示（簡易的なパース）
      // ※バックエンドの返答形式に合わせて調整してください
      setJudgement({
        censure: data.message.split("【救済】")[0].replace("【断罪】", "").trim(),
        remedy: data.message.includes("【救済】") ? data.message.split("【救済】")[1].trim() : ""
      });
    } catch (e) {
      console.error("通信失敗", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-300 flex flex-col items-center justify-center p-4 font-serif">
      <div className="max-w-2xl w-full space-y-8 border border-neutral-800 p-8 relative overflow-hidden">
        {/* 格子の装飾（背景にうっすら） */}
        <div className="absolute inset-0 opacity-5 pointer-events-none" 
             style={{ backgroundImage: 'linear-gradient(90deg, #fff 1px, transparent 1px), linear-gradient(#fff 1px, transparent 1px)', backgroundSize: '40px 40px' }}>
        </div>

        <h1 className="text-2xl text-center tracking-[0.2em] text-neutral-500 uppercase">Confessional</h1>
        
        <div className="space-y-4 relative">
          <textarea
            className="w-full h-40 bg-neutral-900 border border-neutral-700 p-4 text-neutral-200 focus:outline-none focus:border-neutral-500 transition-colors resize-none"
            placeholder="あなたの罪を、ここに..."
            value={confession}
            onChange={(e) => setConfession(e.target.value)}
          />
          
          <button
            onClick={submitConfession}
            disabled={loading}
            className="w-full py-3 border border-neutral-700 hover:bg-neutral-100 hover:text-black transition-all duration-500 tracking-widest uppercase text-sm disabled:opacity-30"
          >
            {loading ? "審理中..." : "告白する"}
          </button>
        </div>

        {judgement.censure && (
          <div className="mt-12 space-y-6 animate-in fade-in duration-1000">
            <div className="border-l-2 border-red-900 pl-4">
              <span className="text-xs text-red-700 uppercase tracking-tighter">断罪</span>
              <p className="mt-1 text-lg leading-relaxed">{judgement.censure}</p>
            </div>
            
            <div className="border-l-2 border-neutral-600 pl-4">
              <span className="text-xs text-neutral-500 uppercase tracking-tighter">救済</span>
              <p className="mt-1 text-sm text-neutral-400 italic">{judgement.remedy}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}