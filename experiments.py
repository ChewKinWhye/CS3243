import numpy as np
import os
from A_star_mod import Puzzle
import os
import sys
import heapq
from Node_mod import Node
from Util import execute_move, state_to_tuple, opposite_move_dict, \
    check_solvable, heuristic_distance_increase, check_valid, get_possible_moves
import time

num_test_cases = 50
n = 3
dirName = "n_equals_" + str(n) + "_test"


class MoveNode:
    def __init__(self, move, prev_move_node):
        self.move = move
        self.prev_move_node = prev_move_node


def create_test_cases():
    input = a = np.arange(n*n)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName,  " Created ")
    else:
        print("Directory ", dirName,  " already exists")
        return 0

    for i in range(num_test_cases):
        np.random.shuffle(input)
        to_save = np.reshape(input, (n, n))
        txt_name = "test_" + str(i+1) + ".txt"
        save_name = os.path.join(dirName, txt_name)
        np.savetxt(save_name, to_save, fmt="%s")


def run_test_cases():
    for i in range(num_test_cases):
        txt_name = "test_" + str(i + 1) + ".txt"
        load_name = os.path.join(dirName, txt_name)
        try:
            f = open(load_name, 'r')
        except IOError:
            raise IOError("Input file not found!")
        lines = f.readlines()
        n = len(lines)
        max_num = n ** 2 - 1
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
        start_time = time.time()
        ans = puzzle.solve()
        elapsed_time = time.time() - start_time
        print("Time taken: " + str(elapsed_time) + " seconds")


# create_test_cases()
run_test_cases()
