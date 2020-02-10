from IDSUtil import get__position_of_number


class IDSNode:
    @classmethod
    def set_goal_state(cls, goal_state):
        cls.goal_state = goal_state

    def __init__(self, state, moves):
        self.state = state
        self.puzzle_size = len(state)
        self.moves = moves

    def get_possible_moves(self):
        x, y = get__position_of_number(self.state, 0)
        moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if x == 0:
            moves.remove('DOWN')
        if x + 1 == self.puzzle_size:
            moves.remove('UP')
        if y == 0:
            moves.remove('RIGHT')
        if y + 1 == self.puzzle_size:
            moves.remove('LEFT')
        return moves

    def __lt__(self, other):
        return self.f_n < other.f_n
