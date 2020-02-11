import sys
from Util_mod import execute_move, check_valid, opposite_move_dict, get_possible_moves, state_to_tuple
import time


class MoveNode:
    def __init__(self, move, prev_move_node):
        self.move = move
        self.prev_move_node = prev_move_node


class Puzzle(object):

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    @staticmethod
    def process_solution(move_node):
        result = []
        while move_node:
            if not move_node.move:
                break
            result.append(move_node.move)
            move_node = move_node.prev_move_node
        result.reverse()
        print("Is valid?")
        print(check_valid(init_state, goal_state, result))
        return [e.value for e in result]

    def solve(self):
        initial_move = MoveNode(None, None)
        next_frontier = [(self.init_state, initial_move)]
        next_visited = {state_to_tuple(self.init_state)}

        cur_depth = 0
        while True:
            cur_depth += 1
            print("Current depth is: " + str(cur_depth))
            cur_visited = next_visited
            next_visited = set()
            frontier = next_frontier
            next_frontier = []
            while frontier:
                cur_state, cur_move_node = frontier.pop()

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
                    if next_state == self.goal_state:
                        result = self.process_solution(MoveNode(move, cur_move_node))
                        return result
                    next_visited.add(next_state_tup)
                    next_move_node = MoveNode(move, cur_move_node)
                    next_frontier.append((next_state, next_move_node))
            if not next_frontier:
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







