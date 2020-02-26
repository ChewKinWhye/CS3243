import gc
import sys
from collections import namedtuple
from Util import execute_move, check_valid, opposite_move_dict, \
    get_possible_moves, state_to_tuple, tuple_to_state, linked_list_to_array, \
    check_solvable
import time

MoveNode = namedtuple("MoveNode", ["move", "prev_move_node"])


class Puzzle(object):

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.total_states_stored = 0

    def process_solution(self, move_node, opp_move_node):
        result = linked_list_to_array(move_node)
        opp_result = linked_list_to_array(opp_move_node)
        opp_result.reverse()
        result.extend(opp_result)

        print("Is valid?", check_valid(self.init_state, self.goal_state, result))
        print("Total states stored: ", self.total_states_stored)
        return [e.value for e in result]

    def solve(self):
        if not check_solvable(self.init_state):
            return ["UNSOLVABLE"]
        n = len(self.init_state)
        initial_move = MoveNode(None, None)
        init_tup = state_to_tuple(self.init_state)
        next_frontier = [(init_tup, initial_move)]
        next_visited = {init_tup: initial_move}

        goal_tup = state_to_tuple(self.goal_state)
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
                cur_state = tuple_to_state(cur_state_tup, n)

                prev_move = cur_move_node.move
                moves = get_possible_moves(cur_state)
                if prev_move:
                    moves.remove(opposite_move_dict[prev_move])

                for move in moves:
                    next_state = execute_move(cur_state, move)
                    next_state_tup = state_to_tuple(next_state)
                    if next_state_tup in cur_visited:
                        continue
                    if next_state_tup in next_visited:
                        continue

                    next_move_node = MoveNode(move, cur_move_node)
                    next_visited[next_state_tup] = next_move_node
                    next_frontier.append((next_state_tup, next_move_node))

            # Opposite side
            opp_cur_visited = opp_next_visited
            opp_next_visited = set()
            opp_frontier = opp_next_frontier
            opp_next_frontier = []
            while opp_frontier:
                cur_state_tup, cur_move_node = opp_frontier.pop()
                cur_state = tuple_to_state(cur_state_tup, n)

                prev_move = cur_move_node.move
                moves = get_possible_moves(cur_state)
                if prev_move:
                    moves.remove(prev_move)

                for move in moves:
                    next_state = execute_move(cur_state, move)
                    next_state_tup = state_to_tuple(next_state)
                    if next_state_tup in opp_cur_visited:
                        continue
                    if next_state_tup in opp_next_visited:
                        continue

                    next_move_node = MoveNode(opposite_move_dict[move], cur_move_node)

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
    start_time = time.time()
    ans = puzzle.solve()
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







