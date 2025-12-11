import tkinter as tk
import random
import winsound  # для звуков на Windows
import time
import json
import os

SAVE_FILE = "2048_save.json"

# Цвета плиток
colors = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.grid_size = 4
        self.score = 0
        self.level = 1

        self.main_grid = tk.Frame(master, bg="#bbada0", bd=3, width=400, height=400)
        self.main_grid.grid(padx=10, pady=10)
        self.make_GUI()
        self.load_game()  # загружаем прогресс, если есть

        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

    # Сохранение прогресса
    def save_game(self):
        data = {
            "matrix": self.matrix,
            "score": self.score,
            "level": self.level
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    # Загрузка сохранённой игры
    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.matrix = data["matrix"]
                self.score = data["score"]
                self.level = data["level"]
            self.update_GUI()
        else:
            self.start_game()

    def make_GUI(self):
        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=colors[0],
                    width=100,
                    height=100
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, text="", bg=colors[0],
                                       justify=tk.CENTER, font=("Helvetica", 24, "bold"), width=4, height=2)
                cell_number.grid(row=i, column=j)
                row.append(cell_number)
            self.cells.append(row)

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.grid()
        self.level_label = tk.Label(self.master, text=f"Level: {self.level}", font=("Helvetica", 16))
        self.level_label.grid()

        # Кнопка рестарта
        restart_button = tk.Button(self.master, text="Restart", command=self.restart_game, font=("Helvetica", 14))
        restart_button.grid(pady=10)

    def start_game(self):
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.add_new_tile()
        self.add_new_tile()
        self.update_GUI()

    def restart_game(self):
        self.score = 0
        self.level = 1
        self.start_game()
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

    def add_new_tile(self):
        empty_cells = [(i,j) for i in range(self.grid_size) for j in range(self.grid_size) if self.matrix[i][j]==0]
        if empty_cells:
            i,j = random.choice(empty_cells)
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4
        winsound.Beep(500, 50)

    def update_GUI(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.matrix[i][j]
                if value == 0:
                    self.cells[i][j].configure(text="", bg=colors[0])
                else:
                    self.cells[i][j].configure(text=str(value), bg=colors[value], fg="#776e65")
        self.score_label.configure(text=f"Score: {self.score}")
        self.level_label.configure(text=f"Level: {self.level}")
        self.master.update_idletasks()

    def stack(self):
        new_matrix = [[0]*self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            fill_position = 0
            for j in range(self.grid_size):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size-1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]
                    winsound.Beep(700, 100)
                    self.cells[i][j].config(font=("Helvetica", 30, "bold"))
                    self.master.update()
                    time.sleep(0.05)
                    self.cells[i][j].config(font=("Helvetica", 24, "bold"))
                    if self.score // 1000 > self.level - 1:
                        self.level += 1

    def reverse(self):
        for i in range(self.grid_size):
            self.matrix[i] = self.matrix[i][::-1]

    def transpose(self):
        self.matrix = [list(row) for row in zip(*self.matrix)]

    def move_left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.save_game()
        self.game_over_check()

    def move_right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.save_game()
        self.game_over_check()

    def move_up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.save_game()
        self.game_over_check()

    def move_down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.save_game()
        self.game_over_check()

    def can_move(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.matrix[i][j] == 0:
                    return True
                if j < self.grid_size-1 and self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
                if i < self.grid_size-1 and self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

    def game_over_check(self):
        if not self.can_move():
            winsound.Beep(300, 500)
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Game Over!", bg="#bbada0", fg="#f00",
                     font=("Helvetica", 30, "bold")).pack()
            self.master.unbind("<Up>")
            self.master.unbind("<Down>")
            self.master.unbind("<Left>")
            self.master.unbind("<Right>")
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)  # удаляем сохранение после окончания игры

# Запуск игры
root = tk.Tk()
game = Game2048(root)
root.mainloop()

