import random
import time

class OTCSimulator:
    def __init__(self, start_price=100.0):
        self.current_price = start_price
        self.trend = 0  # 1 para alta, -1 para baixa, 0 para lateral
        
    def generate_candle(self, timeframe_seconds=60):
        """Gera uma vela completa baseada na dinâmica de OTC"""
        open_price = self.current_price
        high_price = open_price
        low_price = open_price
        
        # Simula o movimento tick a tick dentro da vela
        for _ in range(timeframe_seconds):
            # 70% de chance de seguir a tendência definida
            if random.random() < 0.7 and self.trend != 0:
                move = random.uniform(0, 0.05) * self.trend
            else:
                move = random.uniform(-0.03, 0.03)
                
            self.current_price += move
            
            # Atualiza máxima e mínima do pavio
            if self.current_price > high_price: high_price = self.current_price
            if self.current_price < low_price: low_price = self.current_price
            
        close_price = self.current_price
        
        # Pequena chance de exaustão e mudança de tendência para a próxima vela
        if random.random() < 0.15:
            self.trend = random.choice([-1, 1, 0])
            
        return {
            "open": round(open_price, 5),
            "high": round(high_price, 5),
            "low": round(low_price, 5),
            "close": round(close_price, 5),
            "time": int(time.time())
        }
