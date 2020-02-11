import IDSNode
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


def execute_move(curr_state, move):
    # curr_node = deepcopy(curr_node)
    x, y = get__position_of_number(curr_state, 0)
    new_state = deepcopy(curr_state)
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
