import numpy as np
import random
from itertools import product
from collections import deque


class WumpusAgent:

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.frontier_options = []
        self.cells_without_breeze = deque()
        self.cells_with_breeze = set()

    def update_probabilities_agent(self, probabilities):
        self.frontier_options = probabilities

    def exploring_plan(self, cell, environment):
        # Explora las celdas adyacentes a una celda sin brisa
        adjacents = environment.get_adjacents_cells(cell)
        print("IMPRIMIENDO adyacentes")
        print(adjacents)
        plan = deque()
        for cell in adjacents:
            x = cell[0]
            y = cell[1]
            if not environment.grid[x][y].visited:
                plan.append((x, y))

        return plan

    def choose_actions(self, environment):

        # Posición actual del agente
        x, y = environment.agent_location
        cell = environment.grid[x][y]

        if cell.breeze:
            # Revisa en la pila de celdas exploradas sin brisa
            if len(self.cells_without_breeze) > 0:
                cell_to_go = self.cells_without_breeze.pop()
                return [cell_to_go]

            # Elegir casilla con menos probabilidad si estoy con brisa
            environment.update_probabilities_frontier()
            frontier = environment.get_probability_frontier()

            probabilities = []
            for cell in frontier:
                probabilities.append((cell[0], cell[1], environment.grid[cell[0]][cell[1]].pit_probability))
                print((cell[0], cell[1], environment.grid[cell[0]][cell[1]].pit_probability))

            self.update_probabilities_agent(probabilities)

            minimum = float('inf')

            moves = []
            for tuple in self.frontier_options:
                cell_probability = tuple[2]
                if cell_probability < minimum:
                    minimum = cell_probability
                    moves = [tuple]
                elif cell_probability == minimum:
                    moves.append(tuple)

            if len(moves) > 1:
                return [random.choice(moves)]
            else:
                if len(moves) > 0:
                    return [moves[0]]
        else:  # Casilla sin brisa: Explorar casillas adyacentes
            plan = self.exploring_plan((x, y), environment)
            if len(plan) == 0:
                if len(self.cells_without_breeze) > 0:
                    cell_to_go = self.cells_without_breeze.pop()
                    return [cell_to_go]
                else:
                    return [random.sample(self.cells_with_breeze, 1)]
            else:
                return plan

        # Elegir la próxima acción basada en las probabilidades actuales y la lógica difusa

    # max_prob = np.max(self.knowledge_base)
    # max_indices = np.argwhere(self.knowledge_base == max_prob)

    # Tomar una acción aleatoria entre las celdas con la probabilidad máxima
    # chosen_cell = random.choice(max_indices)

    # En este ejemplo, la acción sería simplemente moverse hacia la celda con mayor probabilidad
    # return {'action': 'move', 'target': chosen_cell}


class Cell:

    def __init__(self,
                 breeze=False,
                 stench=False,
                 gold=False,
                 pit=False,
                 wumpus=False,
                 wall=False):
        self.breeze = breeze
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
        self.knowledge_base = []
        self.pit_probability = 0.2
        self.grid_size = grid_size + 2
        self.grid = [[
            Cell(wall=(i == 0 or i == self.grid_size -
                       1 or j == 0 or j == self.grid_size - 1))
            for j in range(self.grid_size)
        ] for i in range(self.grid_size)]

        # WUMPUS
        x, y = generate_random_tuple(grid_size)
        self.wumpus_location = (x, y)
        self.grid[x][y].wumpus = True
        self.grid[x - 1][y].stench = True
        self.grid[x][y - 1].stench = True
        self.grid[x + 1][y].stench = True
        self.grid[x][y + 1].stench = True
        self.grid[x - 1][y].breeze = True
        self.grid[x][y - 1].breeze = True
        self.grid[x + 1][y].breeze = True
        self.grid[x][y + 1].breeze = True

        # GOLD
        x, y = generate_random_tuple(grid_size)
        self.grid[x][y].gold = True
        self.gold_location = (x, y)

        # PITS
        self.pits_locations = []
        for x in range(1, self.grid_size - 1):
            for y in range(1, self.grid_size - 1):
                if random.random() < self.pit_probability and (x, y) != (
                        1, 1
                ) and x != 0 and y != 0 and x != self.grid_size and y != self.grid_size:
                    self.pits_locations.append((x, y))
                    self.grid[x][y].pit = True
                    self.grid[x - 1][y].breeze = True
                    self.grid[x][y - 1].breeze = True
                    self.grid[x + 1][y].breeze = True
                    self.grid[x][y + 1].breeze = True

        # AGENT
        self.agent_location = (
            1, 1)  # Inicia el agente en la esquina superior izquierda

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
            if self.grid[cell[0]][cell[1]].breeze:
                if (not self.grid[cell[0] - 1][cell[1]].wall) and (
                        not self.grid[cell[0] - 1][cell[1]].visited):
                    frontier.add((cell[0] - 1, cell[1]))

                if (not self.grid[cell[0]][cell[1] - 1].wall) and (
                        not self.grid[cell[0]][cell[1] - 1].visited):
                    frontier.add((cell[0], cell[1] - 1))

                if (not self.grid[cell[0] + 1][cell[1]].wall) and (
                        not self.grid[cell[0] + 1][cell[1]].visited):
                    frontier.add((cell[0] + 1, cell[1]))

                if (not self.grid[cell[0]][cell[1] + 1].wall) and (
                        not self.grid[cell[0]][cell[1] + 1].visited):
                    frontier.add((cell[0], cell[1] + 1))

        return frontier

    def is_there_adjacent(self, array_cells, cell):

        for pit in array_cells:
            x_cell = cell[0]
            y_cell = cell[1]

            x_pit = pit[0]
            y_pit = pit[1]

            if abs(x_cell - x_pit) == 1 and y_cell - y_pit == 0:
                return True
            elif abs(y_cell - y_pit) == 1 and x_cell - x_pit == 0:
                return True
        return False

    def check_config(self, pit_array):
        visited = self.get_visited_cells()
        for aux_cell in visited:
            x_aux = aux_cell[0]
            y_aux = aux_cell[1]
            if self.grid[x_aux][y_aux].breeze:
                if self.is_there_adjacent(pit_array, aux_cell) == False:
                    return False
            else:
                if self.is_there_adjacent(pit_array, aux_cell):
                    return False
        return True

    def calculate_configurations_pit(self, x, y):
        frontier = self.get_probability_frontier()
        # Lista de elementos booleanos
        booleanos = [True, False]

        # Generar todas las combinaciones posibles

        combinaciones = list(product(booleanos, repeat=len(frontier) - 1))
        configuraciones = []
        for combinacion in combinaciones:
            configuracion = []
            posicion_celda = 0
            i = 0
            for celda in frontier:
                if celda[0] == x and celda[1] == y:
                    configuracion.append((celda[0], celda[1]))
                    continue
                if (combinacion[posicion_celda]):
                    configuracion.append((celda[0], celda[1]))

                posicion_celda += 1

            configuraciones.append(configuracion)

        return configuraciones

    def calculate_configurations_no_pit(self, x, y):
        frontier = self.get_probability_frontier()
        # Lista de elementos booleanos
        booleanos = [True, False]

        # Generar todas las combinaciones posibles

        combinaciones = list(product(booleanos, repeat=len(frontier) - 1))
        configuraciones = []
        for combinacion in combinaciones:
            configuracion = []
            posicion_celda = 0
            i = 0
            for celda in frontier:
                if celda[0] == x and celda[1] == y:
                    continue
                if (not combinacion[posicion_celda]):
                    configuracion.append((celda[0], celda[1]))

                posicion_celda += 1

            configuraciones.append(configuracion)

        return configuraciones

    def get_percept(self):
        percept = {
            'stench': False,
            'breeze': False,
            'glitter': False,
            'bump': False,
            'scream': False
        }

        adjacent_cells_wumpus = [
            (self.wumpus_location[0] + 1, self.wumpus_location[1]),
            (self.wumpus_location[0] - 1, self.wumpus_location[1]),
            (self.wumpus_location[0], self.wumpus_location[1] + 1),
            (self.wumpus_location[0], self.wumpus_location[1] - 1)
        ]

        if tuple(self.agent_location) in adjacent_cells_wumpus:
            percept['stench'] = True

        for pit_location in self.pits_locations:
            adjacent_cells_pit = [(pit_location[0] + 1, pit_location[1]),
                                  (pit_location[0] - 1, pit_location[1]),
                                  (pit_location[0], pit_location[1] + 1),
                                  (pit_location[0], pit_location[1] - 1)]
            if tuple(self.agent_location) in adjacent_cells_pit:
                percept['breeze'] = True

        if tuple(self.agent_location) == self.gold_location:
            percept['glitter'] = True

        return percept

    def execute_actions(self, actions, agent):
        while actions:
            print("ACCIONES")
            print(actions)
            action = actions.pop()
            x = action[0]
            y = action[1]
            self.agent_location = (x, y)
            self.grid[x][y].visited = True

            if (not self.grid[x][y].breeze) and len(actions) > 0:
                agent.cells_without_breeze.append((x, y))

            if self.grid[x][y].breeze:
                agent.cells_with_breeze.add((x, y))

            # Verificar condiciones de fin del juego
            if tuple(self.agent_location) == self.wumpus_location:
                print("¡Has perdido! Te encontraste con el Wumpus.")
                return True
            elif tuple(self.agent_location) in self.pits_locations:
                print("¡Has perdido! Caido en un hoyo.")
                return True
            elif tuple(self.agent_location) == self.gold_location:
                print("¡Has ganado! Encontraste el oro.")
                return True

        return False

    def get_valid_configs(self, configs):
        valid_configs = []
        for configuration in configs:
            if self.check_config(configuration):
                valid_configs.append(configuration)
        return valid_configs

    def update_probabilities_frontier(self):
        frontier = self.get_probability_frontier()

        # Calcular las probabilidades de la celda con pozo
        for cell in frontier:
            # print("imprimiendo celda")
            # print(cell)
            config_there_is_pit = self.calculate_configurations_pit(cell[0], cell[1])

            # print("imprimiendo is pit")
            # print(config_there_is_pit)
            config_there_is_no_pit = self.calculate_configurations_no_pit(
                cell[0], cell[1])

            # print("imprimiendo is not pit")
            # print(config_there_is_no_pit)
            # Configuraciones de la frontera válidas con la celda (cell) con pozo
            valid_pit_configs = self.get_valid_configs(config_there_is_pit)
            # print("imprimiendo VALIDAS is pit")
            # print(valid_pit_configs)
            # Configuraciones de la frontera válidas con la celda (cell) sin pozo
            valid_no_pit_configs = self.get_valid_configs(config_there_is_no_pit)
            # print("imprimiendo VALIDAS is not pit")
            # print(valid_no_pit_configs)

            # Calcular probabilidad de que haya pozo
            sum_a = 0
            sum_b = 0

            for config in valid_pit_configs:
                # print("imprimiendo configuración pit")
                # print(config)
                config.remove((cell[0], cell[1]))
                # cada celda con un pozo en la configuración multiplica por 0.2 (priori)
                # print("imprimiendo casillas con pozo PROB SI POZO")
                # print(len(config))
                prob_config = 0.2 ** len(config)
                # cada celda sin un pozo en la configuración multiplica por 0.8 (priori')
                # print("imprimiendo casillas sin pozo PROB si POZO")
                # print(len(frontier) - len(config) - 1)
                prob_config *= 0.8 ** (len(frontier) - len(config) - 1)

                # se suman las probabilidades de cada configuración para el cálculo de la probabilidad de que la celda (cell) contenga un pozo
                sum_a += prob_config

            for config in valid_no_pit_configs:
                # print("imprimiendo configuración no pit")
                # print(config)
                # cada celda con un pozo en la configuración multiplica por 0.2 (priori)
                # print("imprimiendo casillas con pozo PROB NO POZO")
                # print(len(config))
                prob_config = 0.2 ** len(config)
                # cada celda sin un pozo en la configuración multiplica por 0.8 (priori')
                # print("imprimiendo casillas sin pozo PROB NO POZO")
                # print(len(frontier) - len(config) - 1)
                prob_config *= 0.8 ** (len(frontier) - len(config) - 1)

                # se suman las probabilidades de cada configuración para el cálculo de la         probabilidad de que la celda (cell) NO contenga un pozo
                sum_b += prob_config

            prob_a = 0.2 * sum_a
            print("IMPRIMIENDO PROB_A")
            print(prob_a)
            prob_b = 0.8 * sum_b
            print("IMPRIMIENDO PROB_B")
            print(prob_b)

            prob_a_normalized = prob_a / (prob_a + prob_b)
            self.grid[cell[0]][cell[1]].pit_probability = prob_a_normalized
            prob_b_normalized = prob_b / (prob_a + prob_b)

    def get_adjacents_cells(self, cell):
        """
        Devuelve una lista con las celdas vecinas de la celda (cell)
        """
        adjacents = []
        x = cell[0]
        y = cell[1]
        if not self.grid[x - 1][y].wall:
            adjacents.append((x - 1, y))
        if not self.grid[x][y - 1].wall:
            adjacents.append((x, y - 1))
        if not self.grid[x + 1][y].wall:
            adjacents.append((x + 1, y))
        if not self.grid[x][y + 1].wall:
            adjacents.append((x, y + 1))

        return adjacents


def main():
    grid_size = 5
    environment = WumpusEnvironment(grid_size)
    environment.grid[1][1].visited = 1
    '''environment.grid[1][2].visited = 1
    environment.grid[2][1].visited = 1
    environment.grid[1][2].breeze = 1
    environment.grid[2][1].breeze = 1'''
    agent = WumpusAgent(grid_size)

    while True:  # Bucle infinito

        actions = agent.choose_actions(environment)

        # Interacción manual
        print(f"Posición actual del agente: {environment.agent_location}")
        print(f"Posición actual del Wumpus: {environment.wumpus_location}")
        print(f"Posiciones de los agujeros: {environment.pits_locations}")
        print(f"Posición del oro: {environment.gold_location}")
        print(f"Acción elegida: {actions}")
        print(f"Celdas sin brisa: {agent.cells_without_breeze}")

        user_input = input("Presiona Enter para continuar o 'q' para salir: ")

        if user_input.lower() == 'q':
            break

        end_game = environment.execute_actions(actions, agent)

        if end_game:
            break


if __name__ == "__main__":
    main()
