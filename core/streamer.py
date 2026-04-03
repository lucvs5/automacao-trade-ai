# core/streamer.py
import asyncio
import time
from typing import Dict, List

class MarketStreamer:
    def __init__(self):
        # Memória do robô: guarda o histórico das velas
        self.history: List[Dict] = []
        
    async def connect_and_stream(self):
        """
        Simula a conexão com a corretora e o recebimento de velas (candles).
        No futuro, trocaremos isto pelo WebSocket real da sua corretora.
        """
        print("📡 Iniciando conexão com o mercado...")
        await asyncio.sleep(1) # Simula o tempo de carregar
        print("✅ Conectado com sucesso! A receber dados do gráfico...")
        
        # Loop infinito: o robô fica a "ouvir" o mercado sem parar
        while True:
            # Criação de uma vela simulada para alimentar a nossa IA
            mock_candle = {
                "open": 100.0,
                "high": 105.0,
                "low": 98.0,
                "close": 104.0,
                "timestamp": int(time.time()),
                "volume": 500.5
            }
            
            # Adiciona a nova vela ao histórico
            self.history.append(mock_candle)
            
            # Limpa a memória para não travar o computador (guarda só as últimas 20 velas)
            if len(self.history) > 20:
                self.history.pop(0)
                
            # Imprime no terminal para sabermos que está a funcionar
            print(f"📊 Nova vela recebida: Fecho em {mock_candle['close']}")
            
            # Fica em espera 2 segundos até chegar a próxima vela
            await asyncio.sleep(2)
