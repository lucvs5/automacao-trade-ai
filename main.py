# main.py
from fastapi import FastAPI
from core.decision_engine import DoubleSlitLogic

# Aqui criamos o "servidor" do seu projeto
app = FastAPI(title="Automação Trade AI")

@app.get("/")
def read_root():
    """
    Esta é uma rota de teste. Quando aceder ao servidor pelo navegador, 
    esta mensagem vai confirmar que tudo está a funcionar.
    """
    return {
        "status": "Online", 
        "mensagem": "O motor da IA de Trading está a funcionar perfeitamente!"
    }

# Nota do DevMaster: No futuro, adicionaremos aqui as funções de WebSocket 
# para enviar os dados das velas em tempo real diretamente para o Dashboard.
