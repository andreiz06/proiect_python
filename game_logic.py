import random

class GameLogic:
    def __init__(self):
        self.vs_computer = True
        self.reset_game()
        
    def reset_game(self):
        self.board = [""] * 9        
        self.current_player = "X"    
        self.player_symbol = "X"     
        self.game_over = False       
        self.winner = None           
        
    def start_new_game(self, first_player):
        self.reset_game()
        self.player_symbol = first_player
        self.current_player = "X" 
        
    def make_move(self, position):
        if self.game_over or self.board[position]: 
            return False
            
        self.board[position] = self.current_player
        
        if self._check_winner():
            self.winner = self.current_player
            self.game_over = True
        elif self._check_draw():
            self.game_over = True
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            
        return True
        
    def make_computer_move(self):
        if self.game_over:
            return
            
        empty_positions = [i for i, x in enumerate(self.board) if not x]
        if empty_positions:
            position = random.choice(empty_positions)
            self.make_move(position)
            
    def _check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]  
        ]
        
        for combo in win_combinations:
            if (self.board[combo[0]] and
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                return True
        return False
        
    def _check_draw(self):
        return all(self.board)