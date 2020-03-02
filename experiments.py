import numpy as np
import os
import CS3243_P1_07_BFS
import CS3243_P1_07_Linear_Conflict
import CS3243_P1_07_Manhattan_Distance
import CS3243_P1_07_Misplaced_Tiles

import os
import time
num_test_cases = 1000


class MoveNode:
    def __init__(self, move, prev_move_node):
        self.move = move
        self.prev_move_node = prev_move_node


def create_test_cases():
    for n in range(3, 4):
        dirName = "n_equals_" + str(n) + "_test"
        dirName = os.path.join("experiment_data", dirName)
        input = a = np.arange(n * n)
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
    with open("experiment_results.txt", "a") as output_txt:
        output_txt.write("Column 1: Depth of solution\n")
        output_txt.write("Column 2: Total states stored\n")
        output_txt.write("Column 3: Total states searched\n")
        output_txt.write("Column 4: Time taken\n")
    for search_algorithm in range(4):
        n = 3
        experiment_results_n = []
        for i in range(num_test_cases):
            print("Test case", i)
            single_experiment_result = []
            dirName = "n_equals_" + str(n) + "_test"
            dirName = os.path.join("experiment_data", dirName)
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
            if search_algorithm == 0:
                puzzle = CS3243_P1_07_Linear_Conflict.Puzzle(init_state, goal_state)
            elif search_algorithm == 1:
                puzzle = CS3243_P1_07_Manhattan_Distance.Puzzle(init_state, goal_state)
            elif search_algorithm == 2:
                puzzle = CS3243_P1_07_BFS.Puzzle(init_state, goal_state)
            elif search_algorithm == 3:
                puzzle = CS3243_P1_07_Misplaced_Tiles.Puzzle(init_state, goal_state)
            start_time = time.time()
            results = puzzle.solve()
            elapsed_time = time.time() - start_time
            single_experiment_result.extend(puzzle.results)
            single_experiment_result.append(elapsed_time)
            experiment_results_n.append(single_experiment_result)
            # Process experiment results
            experiment_results_n = sorted(experiment_results_n, key=lambda x: x[0])
        for i in range(len(experiment_results_n) - 1, -1, -1):
            result = experiment_results_n[i]
            if len(result) == 1:
                experiment_results_n.pop(i)
        with open("experiment_results.txt", "a") as output_txt:
            if search_algorithm == 0:
                output_txt.write("Testing Linear_Conflict, N = " + str(n) + "\n")
            elif search_algorithm == 1:
                output_txt.write("Testing Manhattan_Distance, N = " + str(n) + "\n")
            elif search_algorithm == 2:
                output_txt.write("Testing BFS, N = " + str(n) + "\n")
            elif search_algorithm == 3:
                output_txt.write("Testing Misplaced_Tiles, N = " + str(n) + "\n")
        with open("experiment_results.txt", "a") as output_txt:
            output_txt.write(str(experiment_results_n) + "\n")


create_test_cases()
run_test_cases()
