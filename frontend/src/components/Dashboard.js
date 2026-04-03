// frontend/src/components/Dashboard.js
import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [level, setLevel] = useState(100);
  const [isAuto, setIsAuto] = useState(false);
  const [systemLog, setSystemLog] = useState(["[SISTEMA] Aguardando início das operações..."]);

  // Função para ligar o robô no Python
  const handleStart = async () => {
    try {
      const response = await fetch('http://localhost:8000/start', { method: 'POST' });
      const data = await response.json();
      
      setIsAuto(true);
      setSystemLog(prev => [...prev, `[SISTEMA] ${data.message}`]);
    } catch (error) {
      setSystemLog(prev => [...prev, "[ERRO] Não foi possível conectar ao servidor backend."]);
    }
  };

  // Função para desligar o robô no Python
  const handleStop = async () => {
    try {
      const response = await fetch('http://localhost:8000/stop', { method: 'POST' });
      const data = await response.json();
      
      setIsAuto(false);
      setSystemLog(prev => [...prev, `[SISTEMA] ${data.message}`]);
    } catch (error) {
      setSystemLog(prev => [...prev, "[ERRO] Falha ao tentar parar a automação."]);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <header className="flex justify-between items-center mb-10 border-b border-slate-700 pb-5">
        <h1 className="text-2xl font-bold text-cyan-400">DEVMASTER PRO | TRADING AI</h1>
        <div className="flex gap-4">
          <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded text-sm">Conta Demo Ativa</span>
          <button className="bg-slate-700 px-4 py-1 rounded hover:bg-slate-600">Sair</button>
        </div>
      </header>

      <main className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Painel de Configurações */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <h2 className="text-lg font-semibold mb-4">Configuração da Espinha Dorsal</h2>
          
          <label className="block mb-2 text-sm text-slate-400">Nível de Raciocínio IA</label>
          <select 
            value={level} 
            onChange={(e) => setLevel(e.target.value)}
            className="w-full bg-slate-900 border border-slate-600 p-2 rounded mb-6"
          >
            <option value={0}>0% - Padrões Diretos</option>
            <option value={50}>50% - Validação de 3 Simetrias</option>
            <option value={100}>100% - Sintetização Completa (5 Simetrias)</option>
          </select>

          <label className="block mb-2 text-sm text-slate-400">Timeframe</label>
          <div className="flex gap-2 mb-6">
            <button className="flex-1 bg-slate-900 p-2 rounded border border-cyan-500 text-cyan-400">1 Min</button>
            <button className="flex-1 bg-slate-900 p-2 rounded border border-slate-600 text-slate-400">5 Min</button>
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

        {/* Visualização de Logs da IA em Tempo Real */}
        <div className="md:col-span-2 bg-black/50 p-4 rounded-xl border border-slate-700 font-mono text-sm overflow-y-auto h-[400px]">
          {systemLog.map((log, index) => (
            <p key={index} className={log.includes("[ERRO]") ? "text-red-400" : "text-cyan-500"}>
              {log}
            </p>
          ))}
          {isAuto && (
            <>
              <p className="text-slate-400">[09:41:02] Buscando Simetrias S1/S2/S3...</p>
              <p className="text-yellow-400">[09:41:05] IA IDENTIFICOU: Raciocínio Ascendente em 100% - Zona Magnética S2 Detectada.</p>
              <p className="text-green-400">[09:41:06] ORDEM EXECUTADA: CALL - Confiança 92% - Mantra: Reversão Consciência.</p>
            </>
          )}
        </div>
      </main>
    </div>
  );
    }
