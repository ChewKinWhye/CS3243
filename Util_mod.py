import Node_mod
from copy import deepcopy
from enum import Enum


class MoveDirection(Enum):
    UP = "UP"           # 0
    DOWN = "DOWN"       # 1
    LEFT = "LEFT"       # 2
    RIGHT = "RIGHT"     # 3


def state_to_tuple(state):
    arr = []
    for row in state:
        for val in row:
            arr.append(val)
    return tuple(arr)


def get__position_of_number(state, number):
    for i, row in enumerate(state):
        for ii, value in enumerate(row):
            if value == number:
                return i, ii


# https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
def check_solvable(state):
    n = len(state)
    inversions = 0
    inversion_is_odd = 0
    if n % 2 == 0:
        blank_row, blank_y = get__position_of_number(state, 0)
        if blank_row % 2 == 0:
            inversion_is_odd = 1
    flat_state = state_to_tuple(state)
    for i, val_i in enumerate(flat_state):
        for j in range(i+1, len(flat_state)):
            if flat_state[j] == 0:
                continue
            if val_i > flat_state[j]:
                inversions += 1
    return inversions % 2 == inversion_is_odd


def heuristic_distance(state, goal_state):
    distance = 0
    state_size = pow(len(state), 2)
    for i in range(1, state_size):
        x1, y1 = get__position_of_number(state, i)
        x2, y2 = get__position_of_number(goal_state, i)
        distance += abs(x1-x2) + abs(y1-y2)
        # not admissible
        # distance += pow(x1 - x2, 2) + pow(y1 - y2, 2)
    return distance


def heuristic_distance_increase(state, goal_state, move):
    n = len(goal_state)
    b_x, b_y = get__position_of_number(state, 0)
    curr_x, curr_y = (-1, -1)
    if move == MoveDirection.UP:
        curr_x, curr_y = (b_x + 1, b_y)
    elif move == MoveDirection.DOWN:
        curr_x, curr_y = (b_x - 1, b_y)
    elif move == MoveDirection.LEFT:
        curr_x, curr_y = (b_x, b_y + 1)
    elif move == MoveDirection.RIGHT:
        curr_x, curr_y = (b_x, b_y - 1)
    next_value = state[curr_x][curr_y]
    g_x = (next_value - 1) // n
    g_y = (next_value - 1) % n

    next_cost = abs(b_x - g_x) + abs(b_y - g_y)
    curr_cost = abs(curr_x - g_x) + abs(curr_y - g_y)

    return next_cost - curr_cost


def execute_move(curr_node, move):
    # curr_node = deepcopy(curr_node)
    x, y = get__position_of_number(curr_node.state, 0)
    new_state = deepcopy(curr_node.state)
    if move == MoveDirection.UP:
        new_state[x][y] = new_state[x + 1][y]
        new_state[x + 1][y] = 0
    elif move == MoveDirection.DOWN:
        new_state[x][y] = new_state[x - 1][y]
        new_state[x - 1][y] = 0
    elif move == MoveDirection.LEFT:
        new_state[x][y] = new_state[x][y + 1]
        new_state[x][y + 1] = 0
    elif move == MoveDirection.RIGHT:
        new_state[x][y] = new_state[x][y - 1]
        new_state[x][y - 1] = 0
    return new_state
    # new_moves = curr_node.moves + (move,)
    # return Node.Node(new_state, new_moves)
