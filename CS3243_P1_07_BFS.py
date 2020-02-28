import gc
import sys
from collections import namedtuple
from copy import deepcopy
import time


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.total_states_stored = 0
        self.start_time = time.time()

        n = len(init_state)
        self.goal_position_map = [0]
        for i in range(1, n * n):
            self.goal_position_map.append(divmod(i - 1, n))

    MoveNode = namedtuple("MoveNode", ["move", "prev_move_node"])

    class MoveDirection:
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    moveDirectionValue = ["UP", "DOWN", "LEFT", "RIGHT"]

    opposite_move_dict = {MoveDirection.UP: MoveDirection.DOWN,
                          MoveDirection.DOWN: MoveDirection.UP,
                          MoveDirection.RIGHT: MoveDirection.LEFT,
                          MoveDirection.LEFT: MoveDirection.RIGHT}

    class Node:
        def __init__(self, state, moves, h_n=None):
            self.state = state
            self.moves = moves
            self.g_n = len(moves)
            self.h_n = h_n
            self.f_n = self.g_n + self.h_n

        def __lt__(self, other):
            return self.f_n < other.f_n

    # https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
    # https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
    @staticmethod
    def check_solvable(state):
        inversions = 0
        inversion_is_odd = 0
        if len(state) % 2 == 0:
            blank_row, blank_y = Puzzle.get_position_of_number(state, 0)
            if blank_row % 2 == 0:
                inversion_is_odd = 1
        flat_state = Puzzle.state_to_tuple(state)
        for i, val_i in enumerate(flat_state):
            for j in range(i + 1, len(flat_state)):
                if flat_state[j] == 0:
                    continue
                if val_i > flat_state[j]:
                    inversions += 1
        return inversions % 2 == inversion_is_odd

    @staticmethod
    def state_to_tuple(state):
        arr = []
        for row in state:
            for val in row:
                arr.append(val)
        return tuple(arr)

    @staticmethod
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

    @staticmethod
    def get_position_of_number(state, number):
        for i, row in enumerate(state):
            for ii, value in enumerate(row):
                if value == number:
                    return i, ii

    @staticmethod
    def get_possible_moves(state):
        MoveDirection = Puzzle.MoveDirection
        x, y = Puzzle.get_position_of_number(state, 0)
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

    # This function takes in the current state and returns the new state
    # after the move has been executed
    @staticmethod
    def execute_move(curr_state, move):
        MoveDirection = Puzzle.MoveDirection
        x, y = Puzzle.get_position_of_number(curr_state, 0)
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

    # This function takes in the initial state and the set of moves
    # and verifies that the moves would reach the goal state
    @staticmethod
    def check_valid(init_state, goal_state, moves):
        for move in moves:
            init_state = Puzzle.execute_move(init_state, move)
        return init_state == goal_state

    @staticmethod
    def linked_list_to_array(move_node):
        result = []
        while move_node is not None:
            if move_node.move is None:
                break
            result.append(move_node.move)
            move_node = move_node.prev_move_node
        result.reverse()
        return result

    def process_solution(self, move_node, opp_move_node):
        elapsed_time = time.time() - self.start_time
        result = Puzzle.linked_list_to_array(move_node)
        opp_result = Puzzle.linked_list_to_array(opp_move_node)
        opp_result.reverse()
        result.extend(opp_result)

        print("Is valid?", Puzzle.check_valid(self.init_state, self.goal_state, result))
        print("Total states stored: ", self.total_states_stored)

        print("Time taken: ", elapsed_time, " seconds")

        return [Puzzle.moveDirectionValue[e] for e in result]

    def solve(self):
        if not Puzzle.check_solvable(self.init_state):
            return ["UNSOLVABLE"]
        n = len(self.init_state)
        initial_move = Puzzle.MoveNode(None, None)
        init_tup = Puzzle.state_to_tuple(self.init_state)
        next_frontier = [(init_tup, initial_move)]
        next_visited = {init_tup: initial_move}

        goal_tup = Puzzle.state_to_tuple(self.goal_state)
        opp_next_frontier = [(goal_tup, initial_move)]
        opp_next_visited = {goal_tup}

        cur_depth = 0
        while True:
            cur_depth += 1
            print("next_visited final size: ", len(next_visited), " opp_: ", len(opp_next_visited))
            self.total_states_stored += len(next_visited) + len(opp_next_visited)
            print("Current depth is: " + str(cur_depth))
            cur_visited = next_visited
            next_visited = {}
            frontier = next_frontier
            next_frontier = []
            gc.collect()
            while frontier:
                cur_state_tup, cur_move_node = frontier.pop()
                cur_state = Puzzle.tuple_to_state(cur_state_tup, n)

                prev_move = cur_move_node.move
                moves = Puzzle.get_possible_moves(cur_state)
                if prev_move:
                    moves.remove(Puzzle.opposite_move_dict[prev_move])

                for move in moves:
                    next_state = Puzzle.execute_move(cur_state, move)
                    next_state_tup = Puzzle.state_to_tuple(next_state)
                    if next_state_tup in cur_visited:
                        continue
                    if next_state_tup in next_visited:
                        continue

                    next_move_node = self.MoveNode(move, cur_move_node)
                    next_visited[next_state_tup] = next_move_node
                    next_frontier.append((next_state_tup, next_move_node))

            # Opposite side
            opp_cur_visited = opp_next_visited
            opp_next_visited = set()
            opp_frontier = opp_next_frontier
            opp_next_frontier = []
            while opp_frontier:
                cur_state_tup, cur_move_node = opp_frontier.pop()
                cur_state = Puzzle.tuple_to_state(cur_state_tup, n)

                prev_move = cur_move_node.move
                moves = Puzzle.get_possible_moves(cur_state)
                if prev_move:
                    moves.remove(prev_move)

                for move in moves:
                    next_state = Puzzle.execute_move(cur_state, move)
                    next_state_tup = Puzzle.state_to_tuple(next_state)
                    if next_state_tup in opp_cur_visited:
                        continue
                    if next_state_tup in opp_next_visited:
                        continue

                    next_move_node = self.MoveNode(Puzzle.opposite_move_dict[move], cur_move_node)

                    if next_state_tup in next_visited:
                        result = self.process_solution(next_visited[next_state_tup], next_move_node)
                        return result
                    if next_state_tup in cur_visited:
                        result = self.process_solution(cur_visited[next_state_tup], next_move_node)
                        return result

                    opp_next_visited.add(next_state_tup)
                    opp_next_frontier.append((next_state_tup, next_move_node))

# python Bfs_search_bidirectional.py n_equals_3/input_2.txt test.txt
if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]


    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







