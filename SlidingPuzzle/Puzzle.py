# 15-sliding Puzzle
class Puzzle:
    def __init__(self, board, goal, level):
        self.board = board
        self.dim = len(board)  # length of the board
        self.level = level  # our g value
        self.goal = goal
        self.f_val = 0  # f_value (for computing g + h values)
        self.error = 0  # total error (for computing heuristics inaccuracy)

    # function to expand a given node (in this case a sliding puzzle board)
    def getNextBoards(self):
        Index = self.board.index("_")  # we can only move a tile around '_' which depicts blank tile
        row = int(Index / 4)  # getting the row and column as we store board as 1 single list
        col = int(Index % 4)

        # we can have 4 legal moves
        up = []
        down = []
        right = []
        left = []
        for el in self.board:
            up.append(el)
            down.append(el)
            right.append(el)
            left.append(el)

        tempBoard = []
        # Move Right
        if (col + 1) < 4:
            ind = row * 4 + (col + 1)
            right[Index], right[ind] = right[ind], right[Index]
            node1 = Puzzle(right, self.goal,
                           self.level + 1)  # creating new Puzzle object with board modified with a right move, also increasing the level with the expansion
            tempBoard.append(node1)

            # Move Left
        if (col - 1) >= 0:
            ind = row * 4 + (col - 1)
            left[Index], left[ind] = left[ind], left[Index]
            node2 = Puzzle(left, self.goal,
                           self.level + 1)  # creating new Puzzle object with board modified with a left move
            tempBoard.append(node2)

        # Move Down
        if (row + 1) < 4:
            ind = (row + 1) * 4 + col
            down[Index], down[ind] = down[ind], down[Index]
            node3 = Puzzle(down, self.goal,
                           self.level + 1)  # creating new Puzzle object with board modified with a down move
            tempBoard.append(node3)

        # Move Up
        if (row - 1) >= 0:
            ind = (row - 1) * 4 + col
            up[Index], up[ind] = up[ind], up[Index]
            node4 = Puzzle(up, self.goal,
                           self.level + 1)  # creating new Puzzle object with board modified with an up move
            tempBoard.append(node4)

        return tempBoard  # returning all newly generated boards (atmost 4)