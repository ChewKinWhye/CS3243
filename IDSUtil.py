import IDSNode
from copy import deepcopy


def get__position_of_number(state, number):
    for i, row in enumerate(state):
        for ii, value in enumerate(row):
            if value == number:
                return i, ii


def execute_move(curr_node, move):
    curr_node = deepcopy(curr_node)
    y, x = get__position_of_number(curr_node.state, 0)
    new_state = curr_node.state
    if move == "DOWN":
        new_state[y][x] = new_state[y+1][x]
        new_state[y+1][x] = 0
    if move == "UP":
        new_state[y][x] = new_state[y-1][x]
        new_state[y-1][x] = 0
    if move == "RIGHT":
        new_state[y][x] = new_state[y][x+1]
        new_state[y][x+1] = 0
    if move == "LEFT":
        new_state[y][x] = new_state[y][x-1]
        new_state[y][x-1] = 0
    new_moves = curr_node.moves
    new_moves.append(move)
    return IDSNode.IDSNode(new_state, new_moves)
