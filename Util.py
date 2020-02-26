from copy import deepcopy
from enum import Enum


class MoveDirection(Enum):
    UP = "UP"           # 0
    DOWN = "DOWN"       # 1
    LEFT = "LEFT"       # 2
    RIGHT = "RIGHT"     # 3


opposite_move_dict = {MoveDirection.UP: MoveDirection.DOWN,
                      MoveDirection.DOWN: MoveDirection.UP,
                      MoveDirection.RIGHT: MoveDirection.LEFT,
                      MoveDirection.LEFT: MoveDirection.RIGHT}


def get_possible_moves(state):
    x, y = get__position_of_number(state, 0)
    puzzle_size = len(state)
    moves = []
    if x != 0:
        moves.append(MoveDirection.DOWN)
    if x + 1 != puzzle_size:
        moves.append(MoveDirection.UP)
    if y != 0:
        moves.append(MoveDirection.RIGHT)
    if y + 1 != puzzle_size:
        moves.append(MoveDirection.LEFT)
    return moves


def state_to_tuple(state):
    arr = []
    for row in state:
        for val in row:
            arr.append(val)
    return tuple(arr)


def tuple_to_state(state_tup, n):
    state = []
    i = 0
    for x in range(n):
        row = []
        for y in range(n):
            row.append(state_tup[i])
            i += 1
        state.append(row)
    return state


def get__position_of_number(state, number):
    for i, row in enumerate(state):
        for ii, value in enumerate(row):
            if value == number:
                return i, ii


last_n_checked_by_get_goal_position = 0
goal_position_map = []


def get_goal_position(number, n):
    global goal_position_map
    global last_n_checked_by_get_goal_position
    if n != last_n_checked_by_get_goal_position:
        goal_position_map = [0]
        for i in range(1, n*n):
            goal_position_map.append(divmod(i - 1, n))
        last_n_checked_by_get_goal_position = n
    return goal_position_map[number]


# https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
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


# Copied https://github.com/Masum95/N-puzzle-solve-using-A-star-search-algorithm/blob/master/State.py
def linear_conflict_row(state, row):
    n = len(state)
    found_goals = []
    for col in range(n):
        found_square = state[row][col]
        if found_square == 0:
            continue
        goal_pos = get_goal_position(found_square, n)
        if goal_pos[0] == row:
            found_goals.append(goal_pos[1])

    for i in range(1,len(found_goals)):
        # Should be strictly increasing.
        if found_goals[i] < found_goals[i-1]:
            return 2
    return 0


def linear_conflict_col(state, col):
    n = len(state)
    found_goals = []
    for row in range(n):
        found_square = state[row][col]
        if found_square == 0:
            continue
        goal_pos = get_goal_position(found_square, n)
        if goal_pos[1] == col:
            found_goals.append(goal_pos[0])

    for i in range(1, len(found_goals)):
        # Should be strictly increasing.
        if found_goals[i] < found_goals[i - 1]:
            return 2
    return 0


def heuristic_distance(state, goal_state):
    distance = 0
    n = len(state)
    state_size = pow(len(state), 2)
    for i in range(1, state_size):
        x1, y1 = get__position_of_number(state, i)
        x2, y2 = get_goal_position(i, n)

        # heuristic 1 admissible and consistent(manhattan dist)
        distance += abs(x1-x2) + abs(y1-y2)

        # heuristic 2 admissible and consistent (misplaced squares)
        # if x1 != x2 or y1 != y2:
        #     distance += 1

        # heuristic 3 not admissible (squared dist)
        # distance += pow(x1 - x2, 2) + pow(y1 - y2, 2)

    # heuristic 1.5 admissible and consistent(linear conflict) when added with manhattan dist
    for row in range(n):
        distance += linear_conflict_row(state, row)
    for col in range(n):
        distance += linear_conflict_col(state, col)

    return distance


def heuristic_distance_increase(state, next_state, move):
    n = len(state)
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
    g_x, g_y = get_goal_position(next_value, n)
    next_cost = 0
    curr_cost = 0

    # heuristic 1 admissible (manhattan dist)
    next_cost += abs(b_x - g_x) + abs(b_y - g_y)
    curr_cost += abs(curr_x - g_x) + abs(curr_y - g_y)

    # heuristic 1.5 admissible and consistent(linear conflict) when added with manhattan dist
    if move == MoveDirection.UP or move == MoveDirection.DOWN:
        if curr_x == g_x:  # next_cost + 1
            next_cost_blank_row = linear_conflict_row(next_state, curr_x)
            if next_cost_blank_row == 0:
                curr_cost += linear_conflict_row(state, curr_x)  # curr_cost_filled_row
        if b_x == g_x:  # next_cost - 1
            curr_cost_blank_row = linear_conflict_row(state, b_x)
            if curr_cost_blank_row == 0:
                next_cost += linear_conflict_row(next_state, b_x)  # next_cost_filled_row
    else:
        if curr_y == g_y:  # next_cost + 1
            next_cost_blank_col = linear_conflict_col(next_state, curr_y)
            if next_cost_blank_col == 0:
                curr_cost += linear_conflict_col(state, curr_y)  # curr_cost_filled_row
        if b_y == g_y:  # next_cost - 1
            curr_cost_blank_col = linear_conflict_col(state, b_y)
            if curr_cost_blank_col == 0:
                next_cost += linear_conflict_col(next_state, b_y)  # next_cost_filled_row

    # heuristic 2 admissible (misplaced squares)
    # if curr_x != g_x or curr_y != g_y:
    #     curr_cost += 1
    # if b_x != g_x and b_y != g_y:
    #     next_cost += 1

    # heuristic 3 not admissible (squared dist)
    # next_cost += pow(b_x - g_x, 2) + pow(b_y - g_y, 2)
    # curr_cost += pow(curr_x - g_x, 2) + pow(curr_y - g_y, 2)

    return next_cost - curr_cost


# This function takes in the current state and returns the new state
# after the move has been executed
def execute_move(curr_state, move):
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
    # new_moves = curr_node.moves + (move,)
    # return Node.Node(new_state, new_moves)


# This function takes in the initial state and the set of moves
# and verifies that the moves would reach the goal state
def check_valid(init_state, goal_state, moves):
    for move in moves:
        init_state = execute_move(init_state, move)
    return init_state == goal_state


def online_solution_check(filename):
    try:
        expected_output_file = filename.replace("input", "expected_output")
        with open(expected_output_file, 'r') as f:
            lines = f.readlines()
            if str(lines[0]) == "No solution":
                print("Online solution: No solution")
            else:
                print("Online solution depth: " + str(lines[0]).rstrip('\n'))
                print("Online solution time taken: " + str(lines[1]) + " seconds")
    except FileNotFoundError:
        print("No expected output")
