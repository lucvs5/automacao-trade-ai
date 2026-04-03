# core/engine.py
from typing import List, Dict

class SymmetryEngine:
    def __init__(self, sensitivity: float = 0.0001):
        self.sensitivity = sensitivity 

    def get_market_state(self, current_candle: Dict, history: List[Dict]) -> str:
        """
        Compila todas as análises para entregar à IA.
        """
        if len(history) < 5:
            return "AGUARDANDO_DADOS"

        # Verifica P4 e P5 (Baseado no seu PDF)
        p4 = self._identify_p4_take_profit(current_candle, history)
        p5 = self._identify_p5_exhaustion(current_candle, history)
        
        if p4: return "P4_DETECTADO"
        if p5: return "P5_DETECTADO"
        
        # Se não for padrão de entrada, verifica simetria básica
        return self._check_s1_symmetry(history)

    def _identify_p4_take_profit(self, current_candle: Dict, history: List[Dict]) -> bool:
        """Regra P4: Família elefante + pavio contra o mercado"""
        last_4_sizes = [abs(c['open'] - c['close']) for c in history[-4:]]
        current_size = abs(current_candle['open'] - current_candle['close'])
        is_elephant = all(current_size > s for s in last_4_sizes)
        
        has_correct_wick = False
        if current_candle['close'] > current_candle['open']: # Alta
            has_correct_wick = (current_candle['high'] - current_candle['close']) > 0
        else: # Baixa
            has_correct_wick = (current_candle['close'] - current_candle['low']) > 0
            
        return is_elephant and has_correct_wick

    def _identify_p5_exhaustion(self, current_candle: Dict, history: List[Dict]) -> bool:
        """Regra P5: Elefante + sequência de 2/3 velas da mesma cor"""
        current_size = abs(current_candle['open'] - current_candle['close'])
        prev_size = abs(history[-1]['open'] - history[-1]['close'])
        
        is_sequence = all(
            (c['close'] > c['open']) == (current_candle['close'] > current_candle['open'])
            for c in history[-2:]
        )
        return current_size > prev_size and is_sequence

    def _check_s1_symmetry(self, history: List[Dict]) -> str:
        """S1: Simetria de corpo com corpo"""
        c1, c2 = history[-2], history[-1]
        if abs(c1['close'] - c2['open']) <= self.sensitivity:
            return "S1_DETECTADA"
        return "SEM_PADRAO"
