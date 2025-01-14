import tkinter as tk
from game_logic import GameLogic

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("800x600")
        self.root.configure(bg="#1A1A2E") 
        
        self.game_logic = GameLogic()
        self.buttons = []  
        self.show_mode_selection()
        
    def show_mode_selection(self):
        self._clear_window()
        mode_frame = self._create_centered_frame()
        
        self._create_title(mode_frame, "TIC TAC TOE", size=32, pady=30)
        self._create_title(mode_frame, "Select Game Mode", size=24, pady=20)
        
        vs_computer = self._create_button(
            mode_frame,
            "Play vs Computer",
            lambda: self.show_symbol_selection(True),
            "#FF6B6B",  
            hover_color="#FF8787"
        )
        vs_computer.pack(pady=10)
        
        
        vs_player = self._create_button(
            mode_frame,
            "Play vs Player",
            lambda: self.show_symbol_selection(False),
            "#4D96FF",  
            hover_color="#6BA6FF"
        )
        vs_player.pack(pady=10)
        
        
        quit_btn = self._create_button(
            mode_frame,
            "Quit Game",
            self.root.quit,  
            "#DC3545",  
            hover_color="#BB2D3B"
        )
        quit_btn.pack(pady=20)
        
    def show_symbol_selection(self, vs_computer):
        self._clear_window()
        self.game_logic.vs_computer = vs_computer
        selection_frame = self._create_centered_frame()
        
        mode_text = "vs Computer" if vs_computer else "vs Player"
        self._create_title(selection_frame, f"Game Mode: {mode_text}", size=24, pady=20)
        self._create_title(selection_frame, "Choose Your Symbol", size=20, pady=15)
        
        x_btn = self._create_button(
            selection_frame,
            "Play as X",
            lambda: self.start_game("X"),
            "#FF6B6B",
            hover_color="#FF8787"
        )
        x_btn.pack(pady=10)
        
        o_btn = self._create_button(
            selection_frame,
            "Play as O",
            lambda: self.start_game("O"),
            "#4D96FF",
            hover_color="#6BA6FF"
        )
        o_btn.pack(pady=10)
        
        back_btn = self._create_button(
            selection_frame,
            "Back",
            self.show_mode_selection,
            "#6C757D",
            hover_color="#5C636A"
        )
        back_btn.pack(pady=10)
        
        
        quit_btn = self._create_button(
            selection_frame,
            "Quit Game",
            self.root.quit,
            "#DC3545",
            hover_color="#BB2D3B"
        )
        quit_btn.pack(pady=10)
        
    def start_game(self, first_player):
        self._clear_window()
        self.game_logic.start_new_game(first_player)
        self.create_game_board()
        
        if self.game_logic.vs_computer and first_player == "O":
            self.game_logic.make_computer_move()
            self._update_board()
            
    def create_game_board(self):
        game_frame = self._create_centered_frame()
        
        self.status_label = tk.Label(
            game_frame,
            text=self._get_status_text(),
            font=("Helvetica", 20, "bold"),
            bg="#1A1A2E",
            fg="#FFFFFF",
            pady=20
        )
        self.status_label.pack()
        
        board_frame = tk.Frame(game_frame, bg="#1A1A2E")
        board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Helvetica", 32, "bold"),
                width=3,
                height=1,
                bg="#2D2D44",
                fg="#FFFFFF",
                activebackground="#3D3D54",
                relief="flat",
                command=lambda x=i: self.handle_click(x)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
            
        control_frame = tk.Frame(game_frame, bg="#1A1A2E")
        control_frame.pack(pady=20)
        
        new_game_btn = self._create_button(
            control_frame,
            "New Game",
            self.show_mode_selection,
            "#4CAF50",
            hover_color="#5DBF61"
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        quit_btn = self._create_button(
            control_frame,
            "Quit Game",
            self.root.quit,
            "#DC3545",
            hover_color="#BB2D3B"
        )
        quit_btn.pack(side=tk.LEFT, padx=10)
        
    def handle_click(self, position):
        if self.game_logic.make_move(position):
            self._update_board()
            
            if not self.game_logic.game_over:
                if self.game_logic.vs_computer:
                    self.game_logic.make_computer_move()
                    self._update_board()
                    
    def _update_board(self):
        board = self.game_logic.board
        for i, symbol in enumerate(board):
            if symbol:
                self.buttons[i].config(
                    text=symbol,
                    fg="#FF6B6B" if symbol == "X" else "#4D96FF",
                    state="disabled"
                )
        self.status_label.config(text=self._get_status_text())
        
        if self.game_logic.game_over:
            for btn in self.buttons:
                btn.config(state="disabled")
                
    def _get_status_text(self):
        if self.game_logic.game_over:
            if self.game_logic.winner:
                if self.game_logic.vs_computer:
                    return "You Win!" if self.game_logic.winner == self.game_logic.player_symbol else "Computer Wins!"
                return f"Player {self.game_logic.winner} Wins!"
            return "It's a Draw!"
            
        current = self.game_logic.current_player
        if self.game_logic.vs_computer:
            return "Your Turn" if current == self.game_logic.player_symbol else "Computer's Turn"
        return f"Player {current}'s Turn"
        
    def _clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def _create_centered_frame(self):
        frame = tk.Frame(self.root, bg="#1A1A2E")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        return frame
        
    def _create_title(self, parent, text, size=24, pady=10):
        return tk.Label(
            parent,
            text=text,
            font=("Helvetica", size, "bold"),
            bg="#1A1A2E",
            fg="#FFFFFF",
            pady=pady
        ).pack()
        
    def _create_button(self, parent, text, command, bg_color, hover_color):
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 16),
            width=15,
            height=2,
            bg=bg_color,
            fg="#FFFFFF",
            activebackground=hover_color,
            activeforeground="#FFFFFF",
            relief="flat",
            command=command
        )
        
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        
        return btn
        
    def run(self):
        self.root.mainloop()