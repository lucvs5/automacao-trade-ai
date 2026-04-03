# core/engine.py
from typing import List, Dict

class SymmetryEngine:
    def __init__(self, sensitivity: float = 0.01):
        self.sensitivity = sensitivity # Margem de erro aceitável para considerar "simetria"

    def analyze_market_state(self, candles: List[Dict]) -> dict:
        """
        Recebe o histórico de velas e retorna o estado das simetrias e movimentos.
        """
        if len(candles) < 5:
            return {"status": "Aguardando mais dados históricos..."}

        latest_candle = candles[-1]
        previous_candles = candles[:-1]

        state = {
            "symmetry": self._check_s1_symmetry(previous_candles),
            "movement": self._check_m1_movement(latest_candle),
            "magnetism_zone": "Consolidação" # Exemplo de estado a ser enviado para IA
        }
        return state

    def _check_s1_symmetry(self, history: List[Dict]) -> str:
        """
        S1 (Rompimento): Simetria de corpo com corpo.
        Compara o Fechamento de uma vela com a Abertura/Fechamento da anterior.
        """
        # Lógica simplificada: Verifica se os corpos das últimas 2 velas estão alinhados
        c1, c2 = history[-2], history[-1]
        
        # Usa a sensibilidade para permitir micro-diferenças na taxa
        if abs(c1['close'] - c2['open']) <= self.sensitivity:
            return "S1_DETECTADA"
        return "SEM_SIMETRIA"

    def _check_m1_movement(self, candle: Dict) -> str:
        """
        M1 (Trator): Movimento contínuo que demonstra força, sem deixar pavio pro lado contrário.
        """
        body_size = abs(candle['open'] - candle['close'])
        
        # Exemplo: Vela de alta (Verde)
        if candle['close'] > candle['open']:
            lower_wick = candle['open'] - candle['low']
            # Se não tem pavio embaixo (ou é menor que 3%), é um movimento Trator de alta
            if lower_wick <= (body_size * 0.03): 
                return "M1_TRATOR_ALTA"
                
        # Exemplo: Vela de baixa (Vermelha)
        elif candle['close'] < candle['open']:
            upper_wick = candle['high'] - candle['open']
            if upper_wick <= (body_size * 0.03):
                return "M1_TRATOR_BAIXA"
                
        return "MOVIMENTO_NORMAL"
