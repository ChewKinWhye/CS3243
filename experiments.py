import numpy as np
import os
import CS3243_P1_07_BFS
import CS3243_P1_07_Linear_Conflict
import CS3243_P1_07_Manhattan_Distance
import CS3243_P1_07_Misplaced_Tiles

import os
import time
import matplotlib.pyplot as plt
num_test_cases = 100


class MoveNode:
    def __init__(self, move, prev_move_node):
        self.move = move
        self.prev_move_node = prev_move_node


def plot_results():
    a = [[11, 141, 200, 0.07983160018920898], [15, 443, 646, 0.13567590713500977], [16, 471, 806, 0.13859105110168457],
         [16, 471, 716, 0.13463997840881348], [17, 755, 1140, 0.17453455924987793],
         [18, 831, 1164, 0.17665410041809082], [18, 831, 1281, 0.16456007957458496],
         [19, 1272, 1738, 0.22523903846740723], [19, 1258, 1838, 0.19947576522827148],
         [20, 1169, 1847, 0.22832894325256348], [20, 1154, 1691, 0.21842002868652344],
         [20, 1169, 1845, 0.21637892723083496], [20, 1350, 1907, 0.22439956665039062],
         [20, 1154, 1924, 0.23636651039123535], [20, 1154, 1679, 0.21839475631713867],
         [21, 2088, 2875, 0.29122304916381836], [21, 2105, 3006, 0.297208309173584],
         [21, 2101, 2938, 0.2871897220611572], [21, 2105, 3390, 0.3101918697357178],
         [22, 1984, 2608, 0.28224754333496094], [22, 1985, 2741, 0.2862725257873535],
         [22, 2011, 3102, 0.3071775436401367], [22, 1984, 3041, 0.32114076614379883],
         [22, 2011, 2693, 0.29040956497192383], [22, 1985, 2815, 0.27525997161865234],
         [23, 3462, 5103, 0.4468653202056885], [23, 3478, 5631, 0.48470449447631836],
         [23, 3449, 5065, 0.41484785079956055], [23, 3478, 5622, 0.426896333694458],
         [23, 3462, 5508, 0.4187929630279541], [23, 3462, 4712, 0.3660585880279541],
         [23, 3449, 4897, 0.3809471130371094], [24, 3163, 4413, 0.3949873447418213],
         [24, 3666, 5344, 0.459972620010376], [24, 3666, 5905, 0.41667985916137695],
         [24, 3186, 4280, 0.35799574851989746], [24, 3163, 4336, 0.3919997215270996],
         [24, 3189, 4743, 0.40591955184936523], [25, 5632, 8488, 0.6143579483032227],
         [25, 5632, 8819, 0.5823431015014648], [25, 5624, 8237, 0.6043875217437744],
         [25, 5632, 8867, 0.5386409759521484], [26, 5369, 7030, 0.623333215713501], [26, 6173, 8354, 0.633307695388794],
         [26, 5355, 7121, 0.5484476089477539], [26, 5355, 7281, 0.5245959758758545],
         [26, 5371, 8154, 0.5704972743988037], [28, 9657, 14038, 0.9982666969299316],
         [28, 8422, 11501, 0.7909154891967773]]
    a = np.asarray(a).T
    plt.plot(a[0], a[1])
    plt.show()


def create_test_cases():
    for n in range(3, 6):
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
        for n in range(3, 6):
            print("N", n)
            experiment_results_n = []
            for i in range(num_test_cases):
                print("Test case", i)
                single_experiment_result = []
                # print("N = ", n)
                # print("Test case = ", str(i+1))
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
            for i in range(len(experiment_results_n)-1, -1, -1):
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
                    output_txt.write("Testing Misplaced_Tiles, N = ", str(n) + "\n")
            with open("experiment_results.txt", "a") as output_txt:
                output_txt.write(str(experiment_results_n) + "\n")
            # experiment_results_n = np.asarray(experiment_results_n).T
            # plt.plot(experiment_results_n[0], experiment_results_n[1])
            # plt.show()


create_test_cases()
run_test_cases()
# plot_results()
