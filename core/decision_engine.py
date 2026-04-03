# core/decision_engine.py

class DoubleSlitLogic:
    """
    Motor que unifica o raciocínio Ascendente e Descendente 
    dentro da 'Espinha Dorsal' da IA.
    """
    
    def __init__(self, patterns, symmetries, movements):
        # Aqui a classe recebe os dados brutos calculados pelo sistema
        self.patterns = patterns
        self.symmetries = symmetries
        self.movements = movements

    def unified_reasoning(self, level_percent: int):
        """
        Executa a lógica baseada no nível de raciocínio escolhido pelo usuário (0%, 50% ou 100%).
        """
        # 1. Raciocínio Descendente (Top-Down)
        # Analisa o campo magnético e as simetrias (S1, S2, S3)
        magnetic_force = self._calculate_magnetic_field()
        
        # 2. Raciocínio Ascendente (Bottom-Up)
        # Analisa o padrão de candle e o movimento (P1-P7 + M1-M3)
        action_potential = self._calculate_pattern_strength()

        # 3. Unificação pela Oitava Inferior (Os Mantras)
        # Aqui a IA decide se a retração é 'equilíbrio' ou 'derrota'
        decision = self._apply_mantras(magnetic_force, action_potential)
        
        return decision

    def _calculate_magnetic_field(self):
        """
        Calcula as forças das simetrias.
        (Por enquanto, deixamos uma resposta padrão para testes).
        """
        return {
            "zone": "BREAKOUT",
            "type": "S1"
        }

    def _calculate_pattern_strength(self):
        """
        Calcula a força do padrão atual e do movimento da vela.
        (Por enquanto, deixamos uma resposta padrão para testes).
        """
        return {
            "pattern": "P4",
            "movement": "M1_TRATOR"
        }

    def _apply_mantras(self, mag_force, act_pot):
        """
        Lógica baseada nos 3 Mantras Primários que você descreveu.
        Mantra 1: Efeito Ping-Pong (Consolidação)
        Mantra 2: Retração = Não ação que antecede a vitória
        Mantra 3: Rompimento = Escapar da zona de derrota
        """
        
        # Aplicação do Mantra 3 (Rompimento)
        # Se a zona for de rompimento e o movimento for trator, fazemos uma compra (CALL)
        if mag_force['zone'] == 'BREAKOUT' and act_pot['movement'] == 'M1_TRATOR':
            return "CALL - SUCESSÃO É O SUSTENTO (Rompimento Validado)"
            
        # Aplicação do Mantra 2 (Retração)
        # Se bater em uma simetria S2 com movimento de explosão, fazemos uma venda (PUT)
        if mag_force['type'] == 'S2' and act_pot['movement'] == 'M2_EXPLOSAO':
            return "PUT - NEGAÇÃO DA DERROTA (Retração Magnética)"

        # Se o gráfico não estiver em uma zona clara, a ordem é esperar (Mantra 1)
        return "WAIT - EQUILÍBRIO DE CONSCIÊNCIA"
