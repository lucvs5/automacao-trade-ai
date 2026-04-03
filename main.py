import asyncio  # <-- CORREÇÃO 1: Adicionado para controlar o tempo do loop
from fastapi import FastAPI, BackgroundTasks
from core.streamer import MarketStreamer
from core.engine import SymmetryEngine
from core.decision_engine import DoubleSlitLogic
from core.ai_agent import AI_Orchestrator
import uvicorn

app = FastAPI()

# Inicialização dos Motores
streamer = MarketStreamer()
engine = SymmetryEngine(sensitivity=0.01)
ai_bot = AI_Orchestrator()

# Estado Global Simples (Para o Dashboard saber o que está acontecendo)
automation_status = {"active": False, "last_decision": "Aguardando início..."}

@app.get("/")
def read_root():
    return {"status": "Online", "system": "DEVMASTER PRO AI"}

@app.post("/start")
async def start_automation(background_tasks: BackgroundTasks):
    """Rota que o botão 'INICIAR' do seu React vai chamar"""
    if not automation_status["active"]:
        automation_status["active"] = True
        # Rodar o loop de mercado em background para não travar a API
        background_tasks.add_task(run_trading_loop)
    return {"message": "Automação Iniciada", "status": automation_status}

@app.post("/stop")
def stop_automation():
    """Rota que o botão 'PARAR' vai chamar"""
    automation_status["active"] = False
    return {"message": "Automação Interrompida", "status": automation_status}

async def run_trading_loop():
    """O Coração do Robô: Onde os componentes se conversam"""
    print("🚀 Loop de Trading Ativado!")
    
    while automation_status["active"]:
        # 1. Captura dado (Simulação do Streamer)
        raw_data = await streamer._receive_mock_tick()
        
        # 2. Engine analisa padrões
        # <-- CORREÇÃO 2: Enviando 5 velas fictícias para o Engine não travar
        mock_history = [
            {"open": 100.0, "close": 100.5, "high": 101.0, "low": 99.0},
            {"open": 100.5, "close": 101.0, "high": 101.5, "low": 100.0},
            {"open": 101.0, "close": 100.8, "high": 101.2, "low": 100.5},
            {"open": 100.8, "close": 99.5,  "high": 101.0, "low": 99.0},
            {"open": 99.5,  "close": 100.0, "high": 100.5, "low": 99.2}
        ]
        
        market_state = engine.analyze_market_state(mock_history)
        
        # Trava de segurança: só tenta tomar decisão se tiver as simetrias
        if "status" in market_state:
            decision = market_state["status"]
        else:
            # 3. DoubleSlitLogic toma a decisão técnica
            logic = DoubleSlitLogic(patterns=market_state, symmetries=market_state['symmetry'], movements=market_state['movement'])
            decision = logic.unified_reasoning(level_percent=100)
        
        # 4. Atualiza o status para o Frontend ler
        automation_status["last_decision"] = decision
        print(f"DEBUG: {decision}")
        
        await asyncio.sleep(2) # Espera 2 segundos para a próxima análise

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
