import pytest

from logic4e import *
from utils4e import expr_handle_infix_ops, count

import os.path
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sys
import search
from PIL import Image, ImageTk

definite_clauses_KB = PropDefiniteKB()
for clause in ['(B & F)==>E',
               '(A & E & F)==>G',
               '(B & C)==>F',
               '(A & B)==>D',
               '(E & F)==>H',
               '(H & I)==>J',
               'A', 'B', 'C']:
    definite_clauses_KB.tell(expr(clause))

from agents import (Wall, Gold, Explorer, Thing, Bump, Glitter,
                    WumpusEnvironment, Pit, Wumpus)


explorer_img = "./assets/explorer.jpeg"  # Replace with the path to your image file
gold_img = "./assets/gold.jpeg"
pit_img = "./assets/pit.png"
wumpus_img = "./assets/wumpus.png"

explorer_image = Image.open(explorer_img)
gold_image = Image.open(gold_img)
pit_image = Image.open(pit_img)
wumpus_image = Image.open(wumpus_img)




class WumpusWorldApp(tk.Tk):
    def __init__(self, world_size):
        super().__init__()
        self.title("Wumpus World")
        self.world_size = world_size
        self.grid_canvas = tk.Canvas(self, width=500, height=500)
        self.grid_canvas.pack()
        self.draw_grid()

    def draw_grid(self):
        cell_size = 500 // self.world_size
        for i in range(self.world_size):
            for j in range(self.world_size):
                x1, y1 = i * cell_size, j * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    def draw_agents(self, grid_world):
        for i in range(1,len(grid_world)-1):
            for j in range(1,len(grid_world[i])-1):
                for obj in grid_world[i][j]:
                    if isinstance(obj, Explorer):
                        # Do something for Breeze
                        print("Handling Explorer:", obj)
                        # Convert the PIL Image to a Tkinter PhotoImage
                        tk_explorer = ImageTk.PhotoImage(explorer_image)
                        label = tk.Label(self, image=tk_explorer)
                        label.pack(padx=10, pady=10)
                    elif isinstance(obj, Pit):
                        # Do something for Pit
                        print("Handling Pit:", obj)
                    elif isinstance(obj, Wumpus):
                        # Do something for Pit
                        print("Handling Wumpus:", obj)

    def update_agent_position(self, x, y, direction):
        cell_size = 500 // self.world_size
        agent_size = cell_size // 2
        self.grid_canvas.delete("agent")
        x1, y1 = (x * cell_size) + agent_size//2, (y * cell_size) + agent_size//2
        x2, y2 = x1 + agent_size, y1 + agent_size
        self.grid_canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="black", tags="agent")

        # Additional code can be added here to indicate the agent's facing direction

if __name__ == "__main__":
    def constant_prog(percept):
        return percept

    app = WumpusWorldApp(world_size=4)  # Assuming a 4x4 grid


    w = WumpusEnvironment(constant_prog)
    
    things_grid = w.get_world()
    app.draw_agents(things_grid)
    print(type(things_grid[0][0][0]))



    app.mainloop()