import tkinter as tk
from tkinter import messagebox
import random
import pickle
import os

# --- Lógica de Generación de Sudoku Simple ---
def generate_sudoku():
    # Base para un Sudoku 9x9 legal
    base  = 3
    side  = base*base

    def pattern(r,c): return (base*(r%base)+r//base+c)%side
    def shuffle(s): return random.sample(s,len(s)) 
    
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,side+1))

    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
    
    # Crear solución y reto (quitando números)
    solution = [row[:] for row in board]
    for _ in range(40): # Nivel de dificultad
        r, c = random.randint(0,8), random.randint(0,8)
        board[r][c] = 0
        
    return board, solution

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku con Checkpoints")
        self.checkpoint_file = "sudoku_checkpoint.pkl"
        
        self.lives = 3
        self.board = []
        self.solution = []
        self.cells = {} # Para guardar las referencias a los inputs de la GUI

        self.setup_ui()
        self.load_or_start_game()

    def setup_ui(self):
        self.info_label = tk.Label(self.master, text=f"Vidas: {self.lives}", font=('Arial', 14))
        self.info_label.pack(pady=10)

        self.grid_frame = tk.Frame(self.master, bg="black", bd=2)
        self.grid_frame.pack(padx=20, pady=20)

        for r in range(9):
            for c in range(9):
                # Usar ValidateCommand para que solo acepten números
                vcmd = (self.master.register(self.validate_input), '%P', r, c)
                entry = tk.Entry(self.grid_frame, width=3, font=('Arial', 18), 
                                 justify='center', validate='key', validatecommand=vcmd)
                entry.grid(row=r, column=c, padx=1, pady=1, ipady=5)
                self.cells[(r, c)] = entry

        tk.Button(self.master, text="Nueva Partida", command=self.reset_game).pack(side="left", padx=20, pady=10)

    def validate_input(self, value, r, c):
        if value == "": return True
        if len(value) > 1 or not value.isdigit() or value == "0":
            return False
        
        # Lógica de validación de jugada
        val = int(value)
        r, c = int(r), int(c)
        
        if val == self.solution[r][c]:
            self.board[r][c] = val
            self.cells[(r,c)].config(fg="blue", state="readonly")
            self.create_checkpoint() # Guardar progreso exitoso
            self.check_win()
        else:
            self.lives -= 1
            self.update_info()
            self.cells[(r,c)].delete(0, tk.END)
            self.create_checkpoint() # Guardar pérdida de vida
            if self.lives <= 0:
                messagebox.showerror("Game Over", "Has perdido todas tus vidas.")
                self.reset_game()
        return True

    def update_info(self):
        self.info_label.config(text=f"Vidas: {self.lives}")

    # --- Lógica de Checkpoints con Pickle ---
    def create_checkpoint(self):
        data = {
            'board': self.board,
            'solution': self.solution,
            'lives': self.lives
        }
        with open(self.checkpoint_file, 'wb') as f:
            pickle.dump(data, f)
        print("Checkpoint guardado.")

    def load_or_start_game(self):
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'rb') as f:
                    data = pickle.load(f)
                self.board = data['board']
                self.solution = data['solution']
                self.lives = data['lives']
                self.refresh_grid()
                self.update_info()
                print("Partida recuperada desde el checkpoint.")
            except:
                self.new_game()
        else:
            self.new_game()

    def new_game(self):
        self.board, self.solution = generate_sudoku()
        self.lives = 3
        self.refresh_grid()
        self.update_info()
        self.create_checkpoint()

    def reset_game(self):
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
        self.new_game()

    def refresh_grid(self):
        for (r, c), entry in self.cells.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            val = self.board[r][c]
            if val != 0:
                entry.insert(0, str(val))
                entry.config(fg="black", state="readonly")
            else:
                entry.config(fg="blue")

    def check_win(self):
        if all(self.board[r][c] != 0 for r in range(9) for c in range(9)):
            messagebox.showinfo("¡Felicidades!", "Has completado el Sudoku.")
            self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()