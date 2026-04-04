import asyncio
import os  # <-- ADICIONE ESSE IMPORT AQUI
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse  # Import adicionado aqui!
from core.streamer import MarketStreamer
from core.engine import SymmetryEngine
from core.decision_engine import DoubleSlitLogic
from core.ai_agent import AI_Orchestrator
from core.market_sim import OTCSimulator
import uvicorn

app = FastAPI()

app_state = {
    "data_source": "SIMULATOR",  # Pode ser "SIMULATOR" ou "REAL"
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

# ROTA ATUALIZADA: Agora ela abre o seu HTML visual
@app.get("/")
async def read_index():
    # Isso descobre a pasta exata onde o seu main.py está rodando
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(diretorio_atual, "index.html")
    
    # Verifica se o arquivo realmente existe antes de enviar
    if not os.path.exists(caminho_html):
        return {"erro": "Arquivo index.html não foi encontrado na mesma pasta do main.py!"}
        
    return FileResponse(caminho_html)

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
