import os
import sys
import heapq
import time
from copy import deepcopy


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.start_time = time.time()
        self.searched_state_count = 0
        self.heuristic_execution_count = 0

        # For consistent heuristic
        self.explored_states = set()

        # For not consistent heuristic
        # self.explored_states = {}

        n = len(init_state)
        self.goal_position_map = [0]
        for i in range(1, n * n):
            self.goal_position_map.append(divmod(i - 1, n))

    ################################ HELPER METHODS ################################

    class MoveDirection:
        UP = 0  # 0
        DOWN = 1  # 1
        LEFT = 2  # 2
        RIGHT = 3  # 3

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

    def heuristic_distance(self, state, goal_state):
        distance = 0
        n = len(state)
        state_size = pow(len(state), 2)
        for i in range(1, state_size):
            x1, y1 = Puzzle.get_position_of_number(state, i)
            x2, y2 = self.get_goal_position(i)

            # heuristic 1 admissible and consistent(manhattan dist)
            distance += abs(x1 - x2) + abs(y1 - y2)

            # heuristic 2 admissible and consistent (misplaced squares)
            # if x1 != x2 or y1 != y2:
            #     distance += 1

            # heuristic 3 not admissible (squared dist)
            # distance += pow(x1 - x2, 2) + pow(y1 - y2, 2)

        # heuristic 1.5 admissible and consistent(linear conflict) when added with manhattan dist
        for row in range(n):
            distance += self.linear_conflict_row(state, row)
        for col in range(n):
            distance += self.linear_conflict_col(state, col)

        return distance

    # Copied https://github.com/Masum95/N-puzzle-solve-using-A-star-search-algorithm/blob/master/State.py
    def linear_conflict_row(self, state, row):
        found_goals = []
        for col in range(len(state)):
            found_square = state[row][col]
            if found_square == 0:
                continue
            goal_pos = self.get_goal_position(found_square)
            if goal_pos[0] == row:
                found_goals.append(goal_pos[1])

        for i in range(1, len(found_goals)):
            # Should be strictly increasing.
            if found_goals[i] < found_goals[i - 1]:
                return 2
        return 0

    def linear_conflict_col(self, state, col):
        found_goals = []
        for row in range(len(state)):
            found_square = state[row][col]
            if found_square == 0:
                continue
            goal_pos = self.get_goal_position(found_square)
            if goal_pos[1] == col:
                found_goals.append(goal_pos[0])

        for i in range(1, len(found_goals)):
            # Should be strictly increasing.
            if found_goals[i] < found_goals[i - 1]:
                return 2
        return 0

    @staticmethod
    def get_position_of_number(state, number):
        for i, row in enumerate(state):
            for ii, value in enumerate(row):
                if value == number:
                    return i, ii

    def get_goal_position(self, number):
        # return divmod(number - 1, n)
        return self.goal_position_map[number]

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

    def heuristic_distance_increase(self, state, next_state, move):
        MoveDirection = Puzzle.MoveDirection
        b_x, b_y = Puzzle.get_position_of_number(state, 0)
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
        g_x, g_y = self.get_goal_position(next_value)
        next_cost = 0
        curr_cost = 0

        # heuristic 1 admissible (manhattan dist)
        next_cost += abs(b_x - g_x) + abs(b_y - g_y)
        curr_cost += abs(curr_x - g_x) + abs(curr_y - g_y)

        # # heuristic 1.5 admissible and consistent(linear conflict) when added with manhattan dist
        # if move == MoveDirection.UP or move == MoveDirection.DOWN:
        #     linear_conflict_row = self.linear_conflict_row
        #     if curr_x == g_x:
        #         next_cost_blank_row = linear_conflict_row(next_state, curr_x)
        #         if next_cost_blank_row == 0:
        #             curr_cost += linear_conflict_row(state, curr_x)
        #     if b_x == g_x:
        #         curr_cost_blank_row = linear_conflict_row(state, b_x)
        #         if curr_cost_blank_row == 0:
        #             next_cost += linear_conflict_row(next_state, b_x)
        # else:
        #     linear_conflict_col = self.linear_conflict_col
        #     if curr_y == g_y:
        #         next_cost_blank_col = linear_conflict_col(next_state, curr_y)
        #         if next_cost_blank_col == 0:
        #             curr_cost += linear_conflict_col(state, curr_y)
        #     if b_y == g_y:
        #         curr_cost_blank_col = linear_conflict_col(state, b_y)
        #         if curr_cost_blank_col == 0:
        #             next_cost += linear_conflict_col(next_state, b_y)

                    # heuristic 2 admissible (misplaced squares)
        # if curr_x != g_x or curr_y != g_y:
        #     curr_cost += 1
        # if b_x != g_x and b_y != g_y:
        #     next_cost += 1

        # heuristic 3 not admissible (squared dist)
        # next_cost += pow(b_x - g_x, 2) + pow(b_y - g_y, 2)
        # curr_cost += pow(curr_x - g_x, 2) + pow(curr_y - g_y, 2)

        return next_cost - curr_cost

    # This function takes in the initial state and the set of moves
    # and verifies that the moves would reach the goal state
    @staticmethod
    def check_valid(init_state, goal_state, moves):
        for move in moves:
            init_state = Puzzle.execute_move(init_state, move)
        return init_state == goal_state

    def process_solution(self, result):
        elapsed_time = time.time() - self.start_time
        print("Solution found at depth: ", len(result))
        print("Is solution valid? ", Puzzle.check_valid(self.init_state, self.goal_state, result))

        print("Time taken: ", elapsed_time, " seconds")

        print("States searched: ", self.searched_state_count)
        print("Times heuristic increase executed: ", self.heuristic_execution_count)
        print("States stored: ", len(self.explored_states))

        return [Puzzle.moveDirectionValue[e] for e in result]

    def solve(self):
        if not self.check_solvable(self.init_state):
            return ["UNSOLVABLE"]

        initial_node = self.Node(self.init_state,
                                 moves=(),
                                 h_n=self.heuristic_distance(self.init_state, self.goal_state))
        frontier = [initial_node]
        explored_states = self.explored_states

        while len(frontier) != 0:
            curr_node = heapq.heappop(frontier)
            curr_dist = curr_node.g_n
            state_tup = Puzzle.state_to_tuple(curr_node.state)

            # For not consistent heuristic
            # found_dist = explored_states.get(state_tup)
            # if found_dist and found_dist < curr_dist:
            #     continue
            # explored_states[state_tup] = curr_node.g_n

            # For consistent heuristic
            if state_tup in explored_states:
                continue
            explored_states.add(state_tup)

            moves = Puzzle.get_possible_moves(curr_node.state)
            if curr_dist > 0:
                prev_move = curr_node.moves[curr_dist - 1]
                moves.remove(Puzzle.opposite_move_dict[prev_move])

            curr_dist += 1
            if curr_node.state == self.goal_state:
                return self.process_solution(curr_node.moves)
            cur_h_n = curr_node.h_n
            for move in moves:
                next_state = Puzzle.execute_move(curr_node.state, move)
                next_state_tup = Puzzle.state_to_tuple(next_state)

                # For consistent heuristic
                if next_state_tup in explored_states:
                    continue
                self.searched_state_count += 1

                # For not consistent heuristic
                # next_found_dist = explored_states.get(next_state_tup)
                # if next_found_dist and next_found_dist <= curr_dist:
                #     continue

                new_moves = curr_node.moves + (move,)
                next_h_n = cur_h_n + self.heuristic_distance_increase(curr_node.state, next_state, move)
                self.heuristic_execution_count += 1
                # For checking consistency
                # if cur_h_n > next_h_n + 1:
                #     print("not consistent! ", heuristic_distance_increase(curr_node.state, next_state, move))
                new_node = Puzzle.Node(next_state, new_moves, next_h_n)
                heapq.heappush(frontier, new_node)
        return ["UNSOLVABLE"]


# python CS3243_P1_07_Linear_Conflict.py n_equals_4/input_3.txt test.txt
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

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')




