#  Universidad del Valle de Guatemala
#  Inteligencia Artificial
#  Eric Mendoza: 15002
#  Proyecto 1: Agente inteligente
#  Puzzle15.py: El presente programa implementa el algoritmo A* para solucionar el 15 puzzle
from AStar import *
import time
from copy import deepcopy


def format_input(raw_puzzle):
    puzzle = [[], [], [], []]
    if len(raw_puzzle) != 16:
        print("Se ha ingresado un puzzle incorrecto.")
        exit(-1)

    index = 0
    for i in range(4):
        for j in range(4):
            value = raw_puzzle[index]
            if value == "A":
                value = 10
            elif value == "B":
                value = 11
            elif value == "C":
                value = 12
            elif value == "D":
                value = 13
            elif value == "E":
                value = 14
            elif value == "F":
                value = 15
            else:
                value = int(value)
            puzzle[i].append(value)
            index += 1

    return puzzle


def print_puzzle(puzzle):
    result = "╔═══════╤═══════╤═══════╤═══════╗\n"
    result += "║\t%s\t│\t%s\t│\t%s\t│\t%s\t║\n" % (puzzle[0][0], puzzle[0][1], puzzle[0][2], puzzle[0][3])
    result += "╟───────┼───────┼───────┼───────╢\n"
    result += "║\t%s\t│\t%s\t│\t%s\t│\t%s\t║\n" % (puzzle[1][0], puzzle[1][1], puzzle[1][2], puzzle[1][3])
    result += "╟───────┼───────┼───────┼───────╢\n"
    result += "║\t%s\t│\t%s\t│\t%s\t│\t%s\t║\n" % (puzzle[2][0], puzzle[2][1], puzzle[2][2], puzzle[2][3])
    result += "╟───────┼───────┼───────┼───────╢\n"
    result += "║\t%s\t│\t%s\t│\t%s\t│\t%s\t║\n" % (puzzle[3][0], puzzle[3][1], puzzle[3][2], puzzle[3][3])
    result += "╚═══════╧═══════╧═══════╧═══════╝\n"
    return result.replace("\t0", "\t ", 1)


# Implementacion para ordenador de palabras
class PuzzleState(State):
    def __init__(self, state, parent, action, start=0, goal=0):
        super(PuzzleState, self).__init__(state, parent, action, start, goal)
        self.heuristic_value = 0
        self.free_position = 0
        self.unallocated_squares = 0

        # Verificar si el problema es resoluble
        if self.action == "Inicio.":
            if not self.is_solvable():
                print("El problema no tiene solucion.")
                exit(-1)

        self.total_cost = self.get_total_cost()  # Calcular el costo de la ruta (heuristica + pathcost)

    # Esta funcion determina si la configuracion es resoluble
    def is_solvable(self):
        # Se deben calcular el numero de inversiones de cada cuadro
        total_inversions = 0
        for row in range(4):
            for column in range(4):
                total_inversions += self.get_inversions(row, column)

        # Sumarle la fila donde se encuentra el espacio vacio
        total_inversions += self.free_position[0] + 1  # Se le suma 1 para que sea 1 - 4
        if total_inversions % 2 == 0:
            return True
        else:
            return False

    def get_vertical_moves(self):
        total_inversions = 0
        for column in range(4):
            for row in range(4):
                total_inversions += self.get_inversions(row, column)

        return total_inversions // 3 + total_inversions % 3

    def get_horizontal_moves(self):
        total_inversions = 0
        for row in range(4):
            for column in range(4):
                total_inversions += self.get_inversions(row, column)

        return total_inversions // 3 + total_inversions % 3

    def get_inversions(self, row, column):
        inversions = 0
        value = self.state[row][column]
        # Save freespace location
        if value == 0:
            self.free_position = (row, column)
            return 0

        if value != 1:  # El 1 nunca tiene inversiones
            # Convertir fila y columna en indice unitario
            index = row * 4 + column
            for index2 in range(index, 16):
                row2 = index2 // 4
                column2 = index2 % 4
                value2 = self.state[row2][column2]
                if value > value2 != 0:
                    inversions += 1

        return inversions

    # f() = path_cost(path) + heuristic(path.end)
    def get_total_cost(self):
        total_cost = len(self.path)  # Cada nodo tiene step_cost = 1

        # MANHATTHAN
        total_manhattan = 0
        for row_index in range(4):
            for column_index in range(4):
                total_manhattan += self.manhattan_distance(row_index, column_index)

        # INVERSE DISTANCE
        horizontal = self.get_horizontal_moves()
        vertical = self.get_vertical_moves()
        ID = horizontal + vertical

        self.heuristic_value = max(total_manhattan, ID)
        return self.heuristic_value + total_cost * 0.4

    def manhattan_distance(self, row, column):
        value = self.state[row][column]
        if value == 0:
            self.free_position = (row, column)  # Guardar la posicion del espacio libre
            return 0

        value -= 1  # Se le quita uno para obtener la posicion ideal
        ideal_row = value // 4  # Si tuviera '7', me daria 1
        ideal_column = value % 4  # Si fuera '7' me daria 3

        # Calcular la distancia desde la posicion actual hacia la ideal
        horizontal = abs(ideal_column - column)
        vertical = abs(ideal_row - row)
        ideal_distance = vertical + horizontal

        value += 1  # Retornarlo a su valor anterior

        # Buscar lineal conflicts
        if ideal_distance != 0:
            if horizontal == 0:
                # Buscar inversiones en la columna
                initial_row = row + 1
                while initial_row <= 3:
                    next_value = self.state[initial_row][column]
                    if value > next_value:
                        if (next_value - 1) % 4 == ideal_column:
                            ideal_distance += 2  # Se penaliza por tener un conflicto
                    initial_row += 1
            elif vertical == 0:
                # Buscar inversiones en la fila
                initial_column = column + 1
                while initial_column <= 3:
                    next_value = self.state[row][initial_column]
                    if value > next_value:
                        # Verificar si este valor deberia estar en esta columna
                        if (next_value - 1) // 4 == ideal_row:
                            ideal_distance += 2  # Se penaliza por tener un conflicto
                    initial_column += 1

        self.unallocated_squares += ideal_distance  # Si no es la solucion, esto no valdra 0
        return ideal_distance

    def generate_frontier(self):
        if not self.frontier:
            # Actions: Las acciones que se pueden tomar a partir de un estado. Devuelve (row, column, value).
            actions = self.actions()
            for action in actions:
                child = self.result(action)
                if child:
                    self.frontier.append(child)

    def result(self, action1):  # Devuelve un nuevo estado a partir de una accion
        new_puzzle = deepcopy(self.state)  # Realizar copia del estado anterior
        free_row = self.free_position[0]
        free_column = self.free_position[1]
        # Obtener el numero del movimiento que provoco este estado
        old_value = self.action.split(" ")[0]
        value = new_puzzle[free_row][free_column]

        if action1 == "LEFT":
            value = new_puzzle[free_row][free_column + 1]
            # no realizar accion si es el mismo numero que el anterior
            if old_value != str(value):
                new_puzzle[free_row][free_column] = value
                new_puzzle[free_row][free_column + 1] = 0
            else:
                return 0

        elif action1 == "RIGHT":
            value = new_puzzle[free_row][free_column - 1]
            # no realizar accion si es el mismo numero que el anterior
            if old_value != str(value):
                new_puzzle[free_row][free_column] = value
                new_puzzle[free_row][free_column - 1] = 0
            else:
                return 0

        elif action1 == "DOWN":
            value = new_puzzle[free_row - 1][free_column]
            # no realizar accion si es el mismo numero que el anterior
            if old_value != str(value):
                new_puzzle[free_row][free_column] = value
                new_puzzle[free_row - 1][free_column] = 0
            else:
                return 0

        elif action1 == "UP":
            value = new_puzzle[free_row + 1][free_column]
            # no realizar accion si es el mismo numero que el anterior
            if old_value != str(value):
                new_puzzle[free_row][free_column] = value
                new_puzzle[free_row + 1][free_column] = 0
            else:
                return 0

        else:
            print("Se creo un estado imposible")
            exit(-1)  # No deberia pasar

        return PuzzleState(new_puzzle, self, "%s TO %s" % (value, action1))

    def goal_test(self):
        return self.unallocated_squares == 0

    def get_path_cost(self):  # Calcula el costo de una ruta
        return len(self.path)

    def get_step_cost(self):  # Devuelve el costo de moverse de un estado a otro (Siempre sera 1 en nuestro caso)
        return 1

    def actions(self):  # Define que acciones se pueden realizar en el presente estado
        actions = []

        free_row = self.free_position[0]
        free_column = self.free_position[1]

        # Horizontal
        if free_column + 1 < 4:
            actions.append("LEFT")
        if free_column - 1 >= 0:
            actions.append("RIGHT")

        # Vertical
        if free_row + 1 < 4:
            actions.append("UP")
        if free_row - 1 >= 0:
            actions.append("DOWN")
        return actions


if __name__ == "__main__":
    print("Ingrese la cadena de puzzle que desea resolver:")
    raw_puzzle = "ABCD9234E81F765."  # input()
    raw_puzzle = raw_puzzle.replace(".", "0")
    puzzle = format_input(raw_puzzle)
    print(print_puzzle(puzzle))
    print("Se ejecutaron los siguientes pasos:")

    solved_puzzle = AStarSolver(PuzzleState, puzzle, 0)
    start = time.time()
    solved_puzzle.solve()
    end = time.time()
    total = end - start
    for i in range(len(solved_puzzle.path)):
        state = solved_puzzle.path[i]
        action = state.action
        puzzle_state = state.state
        print("%d) %s\n" % (i, action) + print_puzzle(puzzle_state))

    print("He tardado %s segundos maestro." % total)
    exit(0)
