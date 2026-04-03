import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [level, setLevel] = useState(100);
  const [isAuto, setIsAuto] = useState(false);
  const [source, setSource] = useState("SIMULATOR");
  const [systemLog, setSystemLog] = useState(["[SISTEMA] Aguardando início..."]);

  useEffect(() => {
    let interval;
    if (isAuto) {
      interval = setInterval(async () => {
        try {
          const response = await fetch('http://localhost:8000/status');
          const data = await response.json();
          setSystemLog(prev => [...prev, `[IA] ${data.last_decision}`]);
        } catch (error) { console.error(error); }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isAuto]);

  const handleSourceChange = async (novaFonte) => {
    try {
      await fetch(`http://localhost:8000/set-source/${novaFonte}`, { method: 'POST' });
      setSource(novaFonte);
      setSystemLog(prev => [...prev, `[SISTEMA] Fonte alterada para: ${novaFonte}`]);
    } catch (error) { console.error(error); }
  };

  const handleStart = async () => {
    await fetch('http://localhost:8000/start', { method: 'POST' });
    setIsAuto(true);
    setSystemLog(prev => [...prev, "[SISTEMA] Automação Iniciada"]);
  };

  const handleStop = async () => {
    await fetch('http://localhost:8000/stop', { method: 'POST' });
    setIsAuto(false);
    setSystemLog(prev => [...prev, "[SISTEMA] Automação Interrompida"]);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <header className="flex justify-between items-center mb-10 border-b border-slate-700 pb-5">
        <h1 className="text-2xl font-bold text-cyan-400">DEVMASTER PRO | TRADING AI</h1>
        <div className="flex gap-4">
          <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded text-sm">Conta Demo Ativa</span>
        </div>
      </header>

      <main className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <h2 className="text-lg font-semibold mb-4">Configurações</h2>
          
          <label className="block mb-2 text-sm text-slate-400">Fonte de Dados</label>
          <div className="flex gap-2 mb-6">
            <button 
              onClick={() => handleSourceChange("SIMULATOR")}
              className={`flex-1 p-2 rounded border ${source === "SIMULATOR" ? "border-cyan-500 text-cyan-400 bg-cyan-500/10" : "border-slate-600 text-slate-400"}`}
            >
              Simulador OTC
            </button>
            <button 
              onClick={() => handleSourceChange("REAL")}
              className={`flex-1 p-2 rounded border ${source === "REAL" ? "border-cyan-500 text-cyan-400 bg-cyan-500/10" : "border-slate-600 text-slate-400"}`}
            >
              Mercado Real
            </button>
          </div>

          <button 
            onClick={isAuto ? handleStop : handleStart}
            className={`w-full py-4 rounded-lg font-bold text-lg transition-all ${
              isAuto ? 'bg-red-500 hover:bg-red-600' : 'bg-cyan-500 hover:bg-cyan-600 text-slate-900'
            }`}
          >
            {isAuto ? 'PARAR AUTOMAÇÃO' : 'INICIAR AUTOMAÇÃO'}
          </button>
        </div>

        <div className="md:col-span-2 bg-black/50 p-4 rounded-xl border border-slate-700 font-mono text-sm overflow-y-auto h-[400px]">
          {systemLog.map((log, index) => (
            <p key={index} className={log.includes("[ERRO]") ? "text-red-400" : log.includes("[IA]") ? "text-yellow-400" : "text-cyan-500"}>
              {log}
            </p>
          ))}
        </div>
      </main>
    </div>
  );
              }
