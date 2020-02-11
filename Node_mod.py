from Util import heuristic_distance, get__position_of_number, MoveDirection


class Node:
    @classmethod
    def set_goal_state(cls, goal_state):
        cls.goal_state = goal_state

    def __init__(self, state, moves, h_n=-1):
        self.state = state
        self.puzzle_size = len(state)
        self.moves = moves
        self.g_n = len(moves)
        if h_n == -1:
            self.h_n = heuristic_distance(self.state, self.goal_state)
        else:
            self.h_n = h_n
        self.f_n = self.g_n + self.h_n

    def get_possible_moves(self):
        x, y = get__position_of_number(self.state, 0)
        moves = []
        if x != 0:
            moves.append(MoveDirection.DOWN)
        if x + 1 != self.puzzle_size:
            moves.append(MoveDirection.UP)
        if y != 0:
            moves.append(MoveDirection.RIGHT)
        if y + 1 != self.puzzle_size:
            moves.append(MoveDirection.LEFT)
        return moves

    def __lt__(self, other):
        return self.f_n < other.f_n
