import os
import sys
import heapq
from Node_mod import Node
from Util_mod import execute_move, state_to_tuple
import time


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        Node.set_goal_state(self.goal_state)
        initial_node = Node(self.init_state, moves=())
        frontier = [initial_node]
        explored_states = {}
        while len(frontier) != 0:
            curr_node = heapq.heappop(frontier)
            curr_dist = curr_node.g_n
            found_dist = explored_states.get(state_to_tuple(curr_node.state))
            # Needed for optimal solution if heuristic_distance is not consistent
            if found_dist and found_dist < curr_dist:
                continue
            curr_dist += 1
            explored_states[state_to_tuple(curr_node.state)] = curr_node.g_n
            moves = curr_node.get_possible_moves()
            # Explore node
            if curr_node.state == goal_state:
                return [e.value for e in curr_node.moves]
            for move in moves:
                next_state = execute_move(curr_node, move)
                # Add to frontier
                next_state_tup = state_to_tuple(next_state)
                next_found_dist = explored_states.get(next_state_tup)
                if next_found_dist and next_found_dist < curr_dist:
                    continue
                new_moves = curr_node.moves + (move,)
                new_node = Node(next_state, new_moves)
                heapq.heappush(frontier, new_node)
        return ["UNSOLVABLE"]

    # you may add more functions if you think is useful


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
    start_time = time.time()
    ans = puzzle.solve()
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')
