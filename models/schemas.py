# models/schemas.py
from pydantic import BaseModel
from typing import Optional

class CandleData(BaseModel):
    """
    Este modelo define o formato obrigatório de uma vela (Candle).
    O Python vai rejeitar qualquer dado que não tenha estas informações.
    """
    open: float      # Preço de Abertura
    high: float      # Preço Máximo
    low: float       # Preço Mínimo
    close: float      # Preço de Fecho
    timestamp: int    # Horário exato da vela
    volume: Optional[float] = None  # Volume (opcional)

class TradeDecision(BaseModel):
    """
    Este modelo define como a IA deve responder após analisar o gráfico.
    Garante que ela sempre envie a Ação, a Confiança e o Motivo.
    """
    action: str        # Deve ser "CALL", "PUT" ou "WAIT"
    confidence: float  # De 0 a 100
    reason: str        # O motivo baseado nos seus Mantras
