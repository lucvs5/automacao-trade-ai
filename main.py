import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # Mudamos para HTMLResponse
from core.streamer import MarketStreamer
from core.engine import SymmetryEngine
from core.decision_engine import DoubleSlitLogic
from core.ai_agent import AI_Orchestrator
from core.market_sim import OTCSimulator
import uvicorn

app = FastAPI()

app_state = {
    "data_source": "SIMULATOR",
    "active": False
}

simulator = OTCSimulator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

streamer = MarketStreamer()
engine = SymmetryEngine(sensitivity=0.01)
ai_bot = AI_Orchestrator()

automation_status = {"active": False, "last_decision": "Aguardando início..."}

# O SEU HTML ESTÁ TODO AQUI DENTRO AGORA! 
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>DEVMASTER PRO AI | OTC Simulator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #060B1A; }
        .gold-gradient { background: linear-gradient(135deg, #F4D03F 0%, #B8860B 100%); }
        .terminal-bg { background-color: rgba(0, 0, 0, 0.7); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="text-white font-sans min-h-screen p-6">
    <div class="max-w-6xl mx-auto">
        <header class="flex justify-between items-center mb-10 border-b border-blue-900/50 pb-6">
            <div>
                <h1 class="text-3xl font-extrabold tracking-tighter text-transparent bg-clip-text gold-gradient">
                    DEVMASTER <span class="text-white">PRO AI</span>
                </h1>
                <p class="text-xs text-blue-400 tracking-[0.2em] uppercase">Symmetry & Resonance Engine</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="h-3 w-3 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-sm font-medium text-gray-400">SERVER ONLINE</span>
            </div>
        </header>

        <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="space-y-6">
                <div class="bg-[#0D1528] border border-blue-900/30 p-6 rounded-2xl shadow-2xl">
                    <h2 class="text-gold font-bold mb-4 flex items-center gap-2">
                        <span class="gold-gradient w-1 h-4 block"></span> CONFIGURAÇÃO
                    </h2>
                    <div class="space-y-4">
                        <button onclick="setSource('SIMULATOR')" id="btn-sim" class="w-full py-3 rounded-xl border border-yellow-600/50 text-yellow-500 font-bold hover:bg-yellow-600/10 transition">
                            MODO SIMULADOR OTC
                        </button>
                        <button onclick="setSource('REAL')" id="btn-real" class="w-full py-3 rounded-xl border border-blue-800 text-blue-700 font-bold opacity-50 cursor-not-allowed">
                            CONTA REAL (BLOQUEADO)
                        </button>
                    </div>
                    <div class="mt-8">
                        <button id="power-btn" onclick="togglePower()" class="w-full gold-gradient text-navy-900 py-5 rounded-2xl font-black text-xl shadow-[0_0_30px_rgba(244,208,63,0.2)] hover:scale-[1.02] transition-transform text-[#060B1A]">
                            INICIAR IA
                        </button>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-2">
                <div class="terminal-bg border border-blue-900/20 rounded-2xl h-[500px] flex flex-col shadow-inner">
                    <div class="flex items-center gap-2 px-4 py-3 border-b border-white/5 bg-white/5">
                        <div class="w-3 h-3 rounded-full bg-red-500/50"></div>
                        <div class="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                        <div class="w-3 h-3 rounded-full bg-green-500/50"></div>
                        <span class="text-[10px] text-gray-500 ml-2 font-mono">LIVE_TRADING_LOG.SYS</span>
                    </div>
                    <div id="log-container" class="p-6 overflow-y-auto font-mono text-sm space-y-2 flex-1 scrollbar-hide">
                        <p class="text-blue-400 animate-pulse">> Sistema pronto para ressonância magnética...</p>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        let active = false;
        const container = document.getElementById('log-container');

        function addLog(text, type = 'info') {
            const colors = { info: 'text-gray-400', ia: 'text-yellow-400 font-bold', sys: 'text-blue-500' };
            const p = document.createElement('p');
            p.className = colors[type];
            p.innerHTML = `<span class="opacity-30">[${new Date().toLocaleTimeString()}]</span> ${text}`;
            container.appendChild(p);
            container.scrollTop = container.scrollHeight;
        }

        async function setSource(s) {
            await fetch(`/set-source/`+s, {method: 'POST'});
            addLog(`FONTE DE DADOS ALTERADA: `+s, 'sys');
        }

        async function togglePower() {
            const btn = document.getElementById('power-btn');
            if(!active) {
                await fetch('/start', {method: 'POST'});
                active = true;
                btn.innerText = 'INTERROMPER';
                btn.className = 'w-full bg-red-600 text-white py-5 rounded-2xl font-black text-xl transition-all shadow-[0_0_30px_rgba(220,38,38,0.3)]';
                addLog('MOTOR DE SIMETRIA ATIVADO', 'sys');
            } else {
                await fetch('/stop', {method: 'POST'});
                active = false;
                btn.innerText = 'INICIAR IA';
                btn.className = 'w-full gold-gradient text-[#060B1A] py-5 rounded-2xl font-black text-xl transition-all';
                addLog('SISTEMA DESLIGADO', 'sys');
            }
        }

        setInterval(async () => {
            if(active) {
                const res = await fetch('/status');
                const data = await res.json();
                if(data.last_decision) addLog(`DECISÃO IA: `+data.last_decision, 'ia');
            }
        }, 1500);
    </script>
</body>
</html>
"""

# ROTA DA PÁGINA PRINCIPAL
@app.get("/", response_class=HTMLResponse)
async def read_index():
    return HTML_DASHBOARD

@app.post("/set-source/{source}")
def set_source(source: str):
    if source in ["SIMULATOR", "REAL"]:
        app_state["data_source"] = source
        return {"status": "success", "source": source}
    return {"status": "error", "message": "Fonte inválida"}

@app.get("/status")
def get_status():
    return {
        "active": app_state["active"],
        "data_source": app_state["data_source"],
        "last_decision": automation_status["last_decision"]
    }

@app.post("/start")
async def start_automation(background_tasks: BackgroundTasks):
    if not app_state["active"]:
        app_state["active"] = True
        background_tasks.add_task(run_trading_loop)
    return {"message": "Automação Iniciada"}

@app.post("/stop")
def stop_automation():
    app_state["active"] = False
    return {"message": "Automação Interrompida"}

async def run_trading_loop():
    print(f"🚀 Loop Ativado usando: {app_state['data_source']}!")
    
    while app_state["active"]:
        try:
            if app_state["data_source"] == "SIMULATOR":
                vela = simulator.generate_candle(60)
                dados_para_analise = [vela] * 5 
            else:
                dados_para_analise = [{"open": 100, "close": 100, "high": 100, "low": 100}] * 5
            
            market_state = engine.analyze_market_state(dados_para_analise)
            
            if "status" in market_state:
                decision = market_state["status"]
            else:
                logic = DoubleSlitLogic(patterns=market_state, symmetries=market_state['symmetry'], movements=market_state['movement'])
                decision = logic.unified_reasoning(level_percent=100)
            
            if app_state["data_source"] == "SIMULATOR":
                automation_status["last_decision"] = f"[OTC] Preço: {vela['close']} | Decisão: {decision}"
            else:
                automation_status["last_decision"] = decision
                
            print(f"DEBUG: {automation_status['last_decision']}")
            
        except Exception as e:
            print(f"Erro no loop: {e}")
            
        await asyncio.sleep(2)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
