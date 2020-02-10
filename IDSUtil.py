import IDSNode
from copy import deepcopy


def get__position_of_number(state, number):
    for i, row in enumerate(state):
        for ii, value in enumerate(row):
            if value == number:
                return i, ii


def execute_move(curr_node, move):
    curr_node = deepcopy(curr_node)
    x, y = get__position_of_number(curr_node.state, 0)
    new_state = curr_node.state
    if move == "UP":
        new_state[x][y] = new_state[x+1][y]
        new_state[x+1][y] = 0
    if move == "DOWN":
        new_state[x][y] = new_state[x-1][y]
        new_state[x-1][y] = 0
    if move == "LEFT":
        new_state[x][y] = new_state[x][y+1]
        new_state[x][y+1] = 0
    if move == "RIGHT":
        new_state[x][y] = new_state[x][y-1]
        new_state[x][y-1] = 0
    new_moves = curr_node.moves
    new_moves.append(move)
    return IDSNode.IDSNode(new_state, new_moves)
