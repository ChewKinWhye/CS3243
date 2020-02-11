from IDSUtil import get__position_of_number, MoveDirection


class IDSNode:
    @classmethod
    def set_goal_state(cls, goal_state):
        cls.goal_state = goal_state

    def __init__(self, state, move, depth):
        self.state = state
        self.move = move
        self.depth = depth

    def get_possible_moves(self):
        x, y = get__position_of_number(self.state, 0)
        puzzle_size = len(self.state)
        moves = []
        if x != 0:
            moves.append(MoveDirection.DOWN)
        if x + 1 != puzzle_size:
            moves.append(MoveDirection.UP)
        if y != 0:
            moves.append(MoveDirection.RIGHT)
        if y + 1 != puzzle_size:
            moves.append(MoveDirection.LEFT)
        return moves

    def __str__(self):
        puzzle_size = len(self.state)
        string = ""
        for y in range(0, puzzle_size):
            for x in range(0, puzzle_size):
                string += ("%d" % (self.state[y][x]))
            string += "\n"

        return string

    # def __lt__(self, other):
    #     return self.f_n < other.f_n
