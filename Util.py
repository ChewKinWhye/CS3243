import Node
from copy import deepcopy


def get__position_of_number(state, number):
    for i, row in enumerate(state):
        for ii, value in enumerate(row):
            if value == number:
                return i, ii


def heuristic_distance(state, goal_state):
    distance = 0
    state_size = pow(len(state), 2)
    for i in range(state_size):
        x1, y1 = get__position_of_number(state, i)
        x2, y2 = get__position_of_number(goal_state, i)
        distance += pow((abs(x1-x2) + abs(y1-y2)), 2)
    return distance


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
    return Node.Node(new_state, new_moves)
