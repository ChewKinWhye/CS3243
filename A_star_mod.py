import os
import sys
import heapq
from Node_mod import Node
from Util import execute_move, state_to_tuple, opposite_move_dict, \
    check_solvable, heuristic_distance_increase, check_valid, get_possible_moves
import time


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

    def process_solution(self, result):
        print("Solution found at depth: ", len(result))
        print("Is solution valid? ", check_valid(self.init_state, self.goal_state, result))

        elapsed_time = time.time() - self.start_time
        print("Time taken: ", elapsed_time, " seconds")

        print("States searched: ", self.searched_state_count)
        print("Times heuristic increase executed: ", self.heuristic_execution_count)
        print("States stored: ", len(self.explored_states))

        return [e.value for e in result]

    def solve(self):
        if not check_solvable(self.init_state):
            return ["UNSOLVABLE"]
        Node.set_goal_state(self.goal_state)
        initial_node = Node(self.init_state, moves=())
        frontier = [initial_node]
        explored_states = self.explored_states

        while len(frontier) != 0:
            curr_node = heapq.heappop(frontier)
            curr_dist = curr_node.g_n
            state_tup = state_to_tuple(curr_node.state)

            # For not consistent heuristic
            # found_dist = explored_states.get(state_tup)
            # if found_dist and found_dist < curr_dist:
            #     continue
            # explored_states[state_tup] = curr_node.g_n

            # For consistent heuristic
            if state_tup in explored_states:
                continue
            explored_states.add(state_tup)

            moves = get_possible_moves(curr_node.state)
            if curr_dist > 0:
                prev_move = curr_node.moves[curr_dist - 1]
                moves.remove(opposite_move_dict[prev_move])

            curr_dist += 1
            if curr_node.state == self.goal_state:
                return self.process_solution(curr_node.moves)
            cur_h_n = curr_node.h_n
            for move in moves:
                next_state = execute_move(curr_node.state, move)
                next_state_tup = state_to_tuple(next_state)
                self.searched_state_count += 1

                # For consistent heuristic
                if next_state_tup in explored_states:
                    continue

                # For not consistent heuristic
                # next_found_dist = explored_states.get(next_state_tup)
                # if next_found_dist and next_found_dist <= curr_dist:
                #     continue

                new_moves = curr_node.moves + (move,)
                next_h_n = cur_h_n + heuristic_distance_increase(curr_node.state, next_state, move)
                self.heuristic_execution_count += 1
                # For checking consistency
                # if cur_h_n > next_h_n + 1:
                #     print("not consistent! ", heuristic_distance_increase(curr_node.state, next_state, move))
                new_node = Node(next_state, new_moves, next_h_n)
                heapq.heappush(frontier, new_node)
        return ["UNSOLVABLE"]


# python A_star_mod.py n_equals_4/input_3.txt test.txt
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
