from Util import heuristic_distance, get__position_of_number, MoveDirection


class Node:
    @classmethod
    def set_goal_state(cls, goal_state):
        cls.goal_state = goal_state

    def __init__(self, state, moves, h_n=None):
        self.state = state
        self.moves = moves
        self.g_n = len(moves)
        self.h_n = h_n
        self.f_n = self.g_n + self.h_n

    def __lt__(self, other):
        return self.f_n < other.f_n
