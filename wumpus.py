import pytest
import time

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

from wumpus_environment import WumpusEnvironmentT


explorer_img = "./assets/explorer.jpeg"  # Replace with the path to your image file
gold_img = "./assets/gold.jpeg"
pit_img = "./assets/pit.png"
wumpus_img = "./assets/wumpus.png"
brisa_img = "./assets/brisa.png"
hedor_img = "./assets/hedor.jpg"

explorer_image = Image.open(explorer_img)
gold_image = Image.open(gold_img)
pit_image = Image.open(pit_img)
wumpus_image = Image.open(wumpus_img)
brisa_image = Image.open(brisa_img)
hedor_image = Image.open(hedor_img)

explorer_image = explorer_image.resize((50, 50), Image.LANCZOS)
gold_image = gold_image.resize((50, 50), Image.LANCZOS)
pit_image = pit_image.resize((50, 50), Image.LANCZOS)
wumpus_image = wumpus_image.resize((50, 50), Image.LANCZOS)
brisa_image = brisa_image.resize((50, 50), Image.LANCZOS)
hedor_image = hedor_image.resize((50, 50), Image.LANCZOS)

class WumpusWorldApp(tk.Tk):
    def __init__(self, world_size):
        super().__init__()
        self.title("Wumpus World")
        self.world_size = world_size
        self.grid_canvas = tk.Canvas(self, width=500, height=500)
        self.grid_canvas.pack()
        self.draw_grid()

        # Initialize PhotoImage objects for agents
        self.tk_explorer = ImageTk.PhotoImage(explorer_image)
        self.tk_gold = ImageTk.PhotoImage(gold_image)
        self.tk_pit = ImageTk.PhotoImage(pit_image)
        self.tk_wumpus = ImageTk.PhotoImage(wumpus_image)
        self.tk_brisa = ImageTk.PhotoImage(brisa_image)
        self.tk_hedor = ImageTk.PhotoImage(hedor_image)
        # Add more PhotoImage objects for other agents if needed

    def draw_grid(self):
        cell_size = 500 // self.world_size
        for i in range(self.world_size):
            for j in range(self.world_size):
                x1, y1 = i * cell_size, j * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    def draw_agents(self, grid_world):
        for i in range(1, len(grid_world) - 1):
            for j in range(1, len(grid_world[i]) - 1):
                num_img = 1
                for obj in grid_world[i][j]:
                    if isinstance(obj, HybridWumpusAgent):
                        # Get the position of the agent in the grid
                        x, y = j - 1, i - 1
                        self.update_agent_position(x, y)
                        # Draw the agent image at the specified position
                        self.grid_canvas.create_image((x + 0.25*num_img) * (500 // self.world_size),
                                                      (y + 0.25*num_img) * (500 // self.world_size),
                                                      anchor=tk.CENTER,
                                                      image=self.tk_explorer)
                        
                    elif isinstance(obj, Gold):
                        # Get the position of the agent in the grid
                        x, y = j - 1, i - 1
                        self.update_agent_position(x, y)
                        # Draw the agent image at the specified position
                        self.grid_canvas.create_image((x + 0.20*num_img) * (500 // self.world_size),
                                                      (y + 0.20*num_img) * (500 // self.world_size),
                                                      anchor=tk.CENTER,
                                                      image=self.tk_gold)
                        
                    elif isinstance(obj, Pit):
                        # Get the position of the agent in the grid
                        x, y = j - 1, i - 1
                        self.update_agent_position(x, y)
                        # Draw the agent image at the specified position
                        self.grid_canvas.create_image((x + 0.20*num_img) * (500 // self.world_size),
                                                      (y + 0.20*num_img) * (500 // self.world_size),
                                                      anchor=tk.CENTER,
                                                      image=self.tk_pit)
                        
                    elif isinstance(obj, Wumpus):
                        # Get the position of the agent in the grid
                        x, y = j - 1, i - 1
                        self.update_agent_position(x, y)
                        # Draw the agent image at the specified position
                        self.grid_canvas.create_image((x + 0.20*num_img) * (500 // self.world_size),
                                                      (y + 0.20*num_img) * (500 // self.world_size),
                                                      anchor=tk.CENTER,
                                                      image=self.tk_wumpus) 
                        
                    elif isinstance(obj, Breeze):
                        # Get the position of the agent in the grid
                        x, y = j - 1, i - 1
                        self.update_agent_position(x, y)
                        # Draw the agent image at the specified position
                        self.grid_canvas.create_image((x + 0.20*num_img) * (500 // self.world_size),
                                                      (y + 0.20*num_img) * (500 // self.world_size),
                                                      anchor=tk.CENTER,
                                                      image=self.tk_brisa) 
                        
                    elif isinstance(obj, Stench):
                        # Get the position of the agent in the grid
                        x, y = j - 1, i - 1
                        self.update_agent_position(x, y)
                        # Draw the agent image at the specified position
                        self.grid_canvas.create_image((x + 0.20*num_img) * (500 // self.world_size),
                                                      (y + 0.20*num_img) * (500 // self.world_size),
                                                      anchor=tk.CENTER,
                                                      image=self.tk_hedor) 
                    num_img += 1


                    # Add similar blocks for other agent types (Pit, Wumpus, etc.)

    def update_agent_position(self, x, y):
        cell_size = 500 // self.world_size
        agent_size = cell_size // 2
        self.grid_canvas.delete("agent")
        x1, y1 = (x * cell_size) + agent_size // 2, (y * cell_size) + agent_size // 2
        x2, y2 = x1 + agent_size, y1 + agent_size
        #self.grid_canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="black", tags="agent")


def update_view():
    things_grid = w.get_world()
    app.draw_agents(things_grid)
    w.step()

if __name__ == "__main__":
    def constant_prog(percept):
        return percept

    app = WumpusWorldApp(world_size=4)  # Assuming a 4x4 grid
    w = WumpusEnvironmentT(4)

    things_grid = w.get_world()
    app.draw_agents(things_grid)
    app.mainloop()

    while True:
        app.after(1000,update_view)
        
   
    
       
        

    



    