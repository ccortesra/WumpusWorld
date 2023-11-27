import numpy as np
import random
from itertools import product


class WumpusAgent:
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def update_probabilities(self, percept):
        # Actualizar las probabilidades en la base de conocimientos según el percepto
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if percept.get('stench', False):
                    # Actualizar la probabilidad de Wumpus
                    self.knowledge_base[i, j] *= 0.8  # Ejemplo: Reducción de probabilidad por el olor
                if percept.get('breeze', False):
                    # Actualizar la probabilidad de agujero
                    self.knowledge_base[i, j] *= 0.9  # Ejemplo: Reducción de probabilidad por la brisa
                if percept.get('glitter', False):
                    # La presencia de oro no afecta las probabilidades, ya que ya se sabe que está en esa celda
                    pass

        # Normalizar las probabilidades para que sumen 1
        self.knowledge_base /= np.sum(self.knowledge_base)

    def choose_action(self):
        print("action")
        # Elegir la próxima acción basada en las probabilidades actuales y la lógica difusa
    # max_prob = np.max(self.knowledge_base)
    # max_indices = np.argwhere(self.knowledge_base == max_prob)

    # Tomar una acción aleatoria entre las celdas con la probabilidad máxima
    # chosen_cell = random.choice(max_indices)

    # En este ejemplo, la acción sería simplemente moverse hacia la celda con mayor probabilidad
    # return {'action': 'move', 'target': chosen_cell}


class Cell:
    def __init__(self, breeze=False, stench=False, gold=False, pit=False, wumpus=False, wall=False):
        self.brezze = breeze
        self.stench = stench
        self.gold = gold
        self.pit = pit
        self.wumpus = wumpus
        self.pit_probability = 0
        self.visited = False
        self.wall = wall


def generate_random_tuple(n):
    while True:
        x = random.randint(1, n)
        y = random.randint(1, n)
        if (x, y) != (1, 1):
            return x, y


class WumpusEnvironment:
    def __init__(self, grid_size):
        self.knowledge_base = [];
        self.pit_probability = 0.2
        self.grid_size = grid_size + 2
        self.grid = [[Cell(wall=(i == 0 or i == self.grid_size - 1 or j == 0 or j == self.grid_size - 1)) for j in
                      range(self.grid_size)] for i in range(self.grid_size)]

        # WUMPUS
        x, y = generate_random_tuple(grid_size)
        self.wumpus_location = (x, y)
        self.grid[x][y].wumpus = True
        self.grid[x - 1][y].stench = True
        self.grid[x][y - 1].stench = True
        self.grid[x + 1][y].stench = True
        self.grid[x][y + 1].stench = True

        # GOLD
        x, y = generate_random_tuple(grid_size)
        self.grid[x][y].gold = True
        self.gold_location = (x, y)

        # PITS
        self.pits_locations = []
        for x in range(1, self.grid_size - 1):
            for y in range(1, self.grid_size - 1):
                if random.random() < self.pit_probability and (x, y) != (
                1, 1) and x != 0 and y != 0 and x != self.grid_size and y != self.grid_size:
                    self.pits_locations.append((x, y))
                    self.grid[x][y].pit = True
                    self.grid[x - 1][y].brezze = True
                    self.grid[x][y - 1].brezze = True
                    self.grid[x + 1][y].brezze = True
                    self.grid[x][y + 1].brezze = True

        # AGENT
        self.agent_location = (1, 1)  # Inicia el agente en la esquina superior izquierda


    def get_breeze_cells(self):
        breeze_cells = []
        for x in range(1, self.grid_size - 2):
            for y in range(1, self.grid_size - 2):
                cell = self.grid[x][y]
                if cell.breeze:
                    breeze_cells.append((x, y))
        return breeze_cells


    def get_visited_cells(self):
        visited_cells = []
        for x in range(1, self.grid_size - 2):
            for y in range(1, self.grid_size - 2):
                cell = self.grid[x][y]
                if cell.visited:
                    visited_cells.append((x, y))

        return visited_cells

    def get_probability_frontier(self):
        visited_cells = self.get_visited_cells()
        frontier = set()
        for cell in visited_cells:
            if self.grid[cell[0]][cell[1]].brezze:
                if (not self.grid[cell[0] - 1][cell[1]].wall) and (not self.grid[cell[0] - 1][cell[1]].visited):
                    frontier.add((cell[0] - 1, cell[1]))

                if (not self.grid[cell[0]][cell[1] - 1].wall) and (not self.grid[cell[0]][cell[1] - 1].visited):
                    frontier.add((cell[0], cell[1] - 1))

                if (not self.grid[cell[0] + 1][cell[1]].wall) and (not self.grid[cell[0] + 1][cell[1]].visited):
                    frontier.add((cell[0] + 1, cell[1]))

                if (not self.grid[cell[0]][cell[1] + 1].wall) and (not self.grid[cell[0]][cell[1] + 1].visited):
                    frontier.add((cell[0], cell[1] + 1))

        return frontier
    
    def is_there_adjacent(self, array_cells, cell):

        for pit in array_cells:
            x_cell = cell[0]
            y_cell = cell[1]

            x_pit = pit[0]
            y_pit = pit[1]

            if abs(x_cell-x_pit) < 1 and y_cell-y_pit == 0:
                return True
            elif abs(y_cell-y_pit) < 1 and x_cell-y_pit == 0:
                return True
        return False       
    
    def check_config(self, pit_array, visited):
        
        for aux_cell in visited:
            x_aux = aux_cell[0]
            y_aux = aux_cell[1]
            if self.grid[x_aux][y_aux].breeze:
                if self.is_there_adjacent(pit_array,aux_cell) == False:
                    return False
            else:
                if self.is_there_adjacent(pit_array,aux_cell):
                    return False
                

    def calculate_configurations_pit(self, x, y):
        frontier = self.get_probability_frontier()
        # Lista de elementos booleanos
        booleanos = [True, False]

        # Generar todas las combinaciones posibles

        combinaciones = list(product(booleanos, repeat=len(frontier)-1))
        print(combinaciones)
        configuraciones = []
        for combinacion  in combinaciones:
            configuracion = []
            posicion_celda = 0
            i = 0
            for celda in frontier:
                if celda[0] == x and celda[1] == y:
                    configuracion.append((celda[0], celda[1]))
                    continue
                if(combinacion[posicion_celda]):
                    configuracion.append((celda[0], celda[1]))

                posicion_celda += 1

            configuraciones.append(configuracion)

        return configuraciones

    def calculate_configurations_no_pit(self, x, y):
        frontier = self.get_probability_frontier()
        # Lista de elementos booleanos
        booleanos = [True, False]

        # Generar todas las combinaciones posibles

        combinaciones = list(product(booleanos, repeat=len(frontier)-1))
        print(combinaciones)
        configuraciones = []
        for combinacion  in combinaciones:
            configuracion = []
            posicion_celda = 0
            i = 0
            for celda in frontier:
                if celda[0] == x and celda[1] == y:
                    continue
                if(not combinacion[posicion_celda]):
                    configuracion.append((celda[0], celda[1]))

                posicion_celda += 1

            configuraciones.append(configuracion)

        return configuraciones




    def get_percept(self):
        percept = {'stench': False, 'breeze': False, 'glitter': False, 'bump': False, 'scream': False}

        adjacent_cells_wumpus = [
            (self.wumpus_location[0] + 1, self.wumpus_location[1]),
            (self.wumpus_location[0] - 1, self.wumpus_location[1]),
            (self.wumpus_location[0], self.wumpus_location[1] + 1),
            (self.wumpus_location[0], self.wumpus_location[1] - 1)
        ]

        if tuple(self.agent_location) in adjacent_cells_wumpus:
            percept['stench'] = True

        for pit_location in self.pits_locations:
            adjacent_cells_pit = [
                (pit_location[0] + 1, pit_location[1]),
                (pit_location[0] - 1, pit_location[1]),
                (pit_location[0], pit_location[1] + 1),
                (pit_location[0], pit_location[1] - 1)
            ]
            if tuple(self.agent_location) in adjacent_cells_pit:
                percept['breeze'] = True

        self.grid[1][1].visited = 1
        self.grid[1][2].visited = 1
        self.grid[2][1].visited = 1
        self.grid[1][2].brezze = 1
        self.grid[2][1].brezze = 1
        if tuple(self.agent_location) == self.gold_location:
            percept['glitter'] = True

        return percept

    def execute_action(self, action):
        # Ejecutar la acción en el entorno y devolver el nuevo percepto
        if action['action'] == 'move':
            self.agent_location = action['target']
            # Verificar si el agente cayó en un agujero
            if tuple(self.agent_location) in self.pit_locations:
                print("¡Has caído en un agujero! Fin del juego.")
                return
        elif action['action'] == 'grab' and self.agent_location == self.gold_location:
            print("¡Has ganado! Has agarrado el oro.")
            return
        elif action['action'] == 'shoot' and self.agent_location == self.wumpus_location:
            print("¡Has ganado! Has derrotado al Wumpus.")
            return
        else:
            print("Acción no válida.")

        percept = self.get_percept()
        return percept


def main():
    grid_size = 4
    environment = WumpusEnvironment(grid_size)
    agent = WumpusAgent(grid_size)

    while True:  # Bucle infinito
        percept = environment.get_percept()
        # agent.update_probabilities(percept)
        frontier = environment.get_probability_frontier()

        for cell in frontier:
            configuraciones_pit = environment.calculate_configurations_pit(cell[0], cell[1])
            configuraciones_no_pit = environment.calculate_configurations_no_pit(cell[0], cell[1])
        action = agent.choose_action()

        # Interacción manual
        print(f"Posición actual del agente: {environment.agent_location}")
        print(f"Posición actual del Wumpus: {environment.wumpus_location}")
        print(f"Posiciones de los agujeros: {environment.pits_locations}")
        print(f"Posición del oro: {environment.gold_location}")
        print(f"Percepto actual: {percept}")
        print(f"Acción elegida: {action}")

        user_input = input("Presiona Enter para continuar o 'q' para salir: ")

        if user_input.lower() == 'q':
            break

        percept = environment.execute_action(action)

        # Verificar condiciones de fin del juego
        if tuple(environment.agent_location) == environment.wumpus_location:
            print("¡Has perdido! Te encontraste con el Wumpus.")
            break
        elif tuple(environment.agent_location) in environment.pit_locations:
            print("¡Has perdido! Caido en un hoyo.")
            break
        elif tuple(environment.agent_location) == environment.gold_location:
            print("¡Has ganado! Encontraste el oro.")
            break


if __name__ == "__main__":
    main()
