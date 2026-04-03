import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from core.streamer import MarketStreamer
from core.engine import SymmetryEngine
from core.decision_engine import DoubleSlitLogic
from core.ai_agent import AI_Orchestrator
from core.market_sim import OTCSimulator  # <-- O IMPORT ENTRA AQUI
import uvicorn

app = FastAPI()

# 🟢 ESTADO GLOBAL E SIMULADOR ENTRAM AQUI:
app_state = {
    "data_source": "SIMULATOR",  # Pode ser "SIMULATOR" ou "REAL"
    "active": False
}

simulator = OTCSimulator()

# Liberando o acesso para o Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização dos Motores
streamer = MarketStreamer()
engine = SymmetryEngine(sensitivity=0.01)
ai_bot = AI_Orchestrator()

# Estado Global Simples
automation_status = {"active": False, "last_decision": "Aguardando início..."}

# Continuação do seu main.py...

@app.get("/")
def read_root():
    return {"status": "Online", "system": "DEVMASTER PRO AI"}

@app.post("/set-source/{source}")
def set_source(source: str):
    """Muda a fonte: SIMULATOR ou REAL"""
    if source in ["SIMULATOR", "REAL"]:
        app_state["data_source"] = source
        return {"status": "success", "source": source}
    return {"status": "error", "message": "Fonte inválida"}

@app.get("/status")
def get_status():
    """O site consulta isso a cada 1 segundo"""
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
            # 1. Busca os dados baseado na sua escolha
            if app_state["data_source"] == "SIMULATOR":
                # Gera uma vela simulada de 1 minuto
                vela = simulator.generate_candle(60)
                dados_para_analise = [vela] * 5 # Multiplicamos por 5 para o engine não travar por falta de dados
            else:
                # Aqui entrará a conexão real com a corretora depois
                dados_para_analise = [{"open": 100, "close": 100, "high": 100, "low": 100}] * 5
            
            # 2. IA Analisa
            market_state = engine.analyze_market_state(dados_para_analise)
            
            if "status" in market_state:
                decision = market_state["status"]
            else:
                logic = DoubleSlitLogic(patterns=market_state, symmetries=market_state['symmetry'], movements=market_state['movement'])
                decision = logic.unified_reasoning(level_percent=100)
            
            # 3. Atualiza o que vai para a tela
            if app_state["data_source"] == "SIMULATOR":
                automation_status["last_decision"] = f"[OTC] Preço: {vela['close']} | Decisão: {decision}"
            else:
                automation_status["last_decision"] = decision
                
            print(f"DEBUG: {automation_status['last_decision']}")
            
        except Exception as e:
            print(f"Erro no loop: {e}")
            
        await asyncio.sleep(2) # Pausa de 2 segundos entre ciclos

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
