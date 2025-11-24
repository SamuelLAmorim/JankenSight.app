def determine_winner(move1, move2):
    """
    Determina o vencedor de uma rodada de Pedra, Papel, Tesoura.

    Args:
        move1 (str): Movimento do Jogador 1 (rock, paper, scissors)
        move2 (str): Movimento do Jogador 2 / IA (rock, paper, scissors)

    Returns:
        str: 'Player 1 Wins!', 'Player 2/IA Wins!', ou 'Tie'
    """
    
    # Padroniza para minúsculas para garantir a comparação
    m1 = move1.lower()
    m2 = move2.lower()
    
    if m1 == m2:
        return 'Tie'

    # Condições de vitória para o Jogador 1
    elif (m1 == 'rock' and m2 == 'scissors') or \
         (m1 == 'scissors' and m2 == 'paper') or \
         (m1 == 'paper' and m2 == 'rock'):
        return 'Player 1 Wins!'
        
    # Condições de vitória para o Jogador 2 / IA
    else:
        return 'Player 2/IA Wins!'


class Score:
    def __init__(self):
        self.p1 = 0
        self.p2 = 0 

    def update(self, result):
        if 'Player 1 Wins' in result:
            self.p1 += 1
        elif 'Player 2/IA Wins' in result:
            self.p2 += 1

    def __str__(self):
        return f"Placar: Jog 1: {self.p1} | Jog 2/IA: {self.p2}"
    
    def get_scores(self):
        return self.p1, self.p2
    

    