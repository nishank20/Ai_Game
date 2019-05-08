#  Universidad del Valle de Guatemala
#  Inteligencia Artificial
#  Eric Mendoza: 15002
#  Proyecto 1: Agente inteligente
#  Sudoku.py: El presente programa implementa el algoritmo A* para solucionar Sudokus de 4x4
import time
from AStar import *
from copy import deepcopy


def format_input(raw_sudoku):
    sudoku = [[], [], [], [], [], [], [], [], []]
    if len(raw_sudoku) != 81:
        print("Se ha ingresado un sudoku incorrecto.")
        exit(-1)

    index = 0
    for i in range(9):
        for j in range(9):
            sudoku[i].append(raw_sudoku[index])
            index += 1

    return sudoku


def print_sudoku(sudoku1):
    result = "╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗\n"

    for row in sudoku1:
        result += "║"
        for column in row:
            result += " %s │" % column
        result += "\n"
        result += "╟───┼───┼───┼───┼───┼───┼───┼───┼───╢\n"
    return result


# Implementacion para ordenador de palabras
class SudokuState(State):
    def __init__(self, state, parent, action, start=0, goal=0):
        super(SudokuState, self).__init__(state, parent, action, start, goal)
        self.heuristic_value = 0
        self.free_spaces = 81  # Valor inicial sin sentido, solo no tiene que ser 0

        # Create preemptive_set vacio
        self.preemptive_set = []  # Posibles numeros para cada casilla vacia
        for k in range(9):
            new_row = []
            for j in range(9):
                new_row.append(0)
            self.preemptive_set.append(new_row)

        self.total_cost = self.get_total_cost()  # Calcular el costo de la ruta (heuristica + pathcost)

    # f() = path_cost(path) + heuristic(path.end)
    def get_total_cost(self):
        total_cost = len(self.path)  # Cada nodo tiene step_cost = 1

        # Calcular la heuristica = cantidad de posibles valores a colocar
        self.generate_preemptive_set()

        return total_cost + self.heuristic_value

    # Esta funcion busca todos los espacios vacios. Por cada uno busca  los numeros que se podrían colocar en dicho
    # espacio y los guarda en el conjunto predictivo.
    def generate_preemptive_set(self):
        # Recorrer todos los cuadros para ver los vacios, y por cada uno, ver los posibles numeros
        free_spaces = 0
        for row_index in range(len(self.state)):
            row = self.state[row_index]
            for column_index in range(len(row)):
                space = row[column_index]  # Obtener el espacio
                if space == ".":
                    free_spaces = free_spaces + 1
                    self.preemptive_set[row_index][column_index] = self.get_posible_numbers(row_index, column_index)

        self.free_spaces = free_spaces

    def get_posible_numbers(self, row1, column1):
        posible_numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

        # Check row
        row = self.state[row1]
        for value in row:
            posible_numbers -= {value}

        # Check column
        for row in range(9):
            posible_numbers -= {self.state[row][column1]}

        # Check block
        block_size = 3
        block_row = row1//block_size
        block_column = column1 // block_size

        for row in range(block_row * block_size, block_size * (block_row + 1)):
            for column in range(block_column * block_size, block_size * (block_column + 1)):
                posible_numbers -= {self.state[row][column]}

        sub_heuristic_value = len(posible_numbers)

        if sub_heuristic_value == 0:
            sub_heuristic_value = 100  # Si ya no hay posibles numeros para una casilla vacia, se evita este estado

        self.heuristic_value += sub_heuristic_value ** 2  # Sumar los posibles numeros al cuadrado para favorecer los 1
        return posible_numbers

    def generate_frontier(self):
        if not self.frontier:
            # Actions: Las acciones que se pueden tomar a partir de un estado. Devuelve (row, column, value).
            actions = self.actions()
            for action in actions:
                child = self.result(action)
                self.frontier.append(child)

    def result(self, action):  # Devuelve un nuevo estado a partir de una accion
        new_sudoku = deepcopy(self.state)  # Realizar copia del estado anterior
        new_sudoku[action[0]][action[1]] = action[2]
        return SudokuState(new_sudoku, self, self.to_string_action(action))

    def goal_test(self):
        return self.free_spaces == 0

    def get_path_cost(self):  # Calcula el costo de una ruta
        return len(self.path)

    def get_step_cost(self):  # Devuelve el costo de moverse de un estado a otro (Siempre sera 1 en nuestro caso)
        return 1

    def actions(self):  # Define que acciones se pueden realizar en el presente estado
        actions = []
        for row_index in range(len(self.preemptive_set)):
            row = self.preemptive_set[row_index]
            for column_index in range(len(row)):
                preemptive_set = row[column_index]
                if preemptive_set:
                    # Detener la generacion de acciones si solamente hay una posible accion
                    if len(preemptive_set) == 1:
                        return [(row_index, column_index, preemptive_set.pop())]
                    elif len(preemptive_set) == 2:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    elif len(preemptive_set) == 3:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    elif len(preemptive_set) == 4:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    elif len(preemptive_set) == 5:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    elif len(preemptive_set) == 6:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    elif len(preemptive_set) == 7:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    elif len(preemptive_set) == 8:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
                        return actions
                    else:
                        for value in preemptive_set:
                            actions.append((row_index, column_index, value))
        return actions

    @staticmethod
    def to_string_action(action):
        return "Agregar %s en posicion (%s, %s)" % (action[2], action[0], action[1])


if __name__ == "__main__":
    print("Ingrese la cadena de Sudoku que desea resolver:")
    raw_sudoku1 = "5.......3.7.4...514..16.7..3...1..8...........5..7...2..7.39..892...8.3.8.......4"  # input()
    sudoku = format_input(raw_sudoku1)
    print(print_sudoku(sudoku))
    print("Se ejecutaron los siguientes pasos:")

    solved_sudoku = AStarSolver(SudokuState, sudoku, 0)
    start = time.time()
    solved_sudoku.solve()
    end = time.time()
    total = end - start
    for i in range(len(solved_sudoku.path)):
        state = solved_sudoku.path[i]
        action = state.action
        sudoku_state = state.state
        print("%d) %s\n" % (i, action) + print_sudoku(sudoku_state))

    print("He tardado %s segundos maestro." % total)
    exit(0)
