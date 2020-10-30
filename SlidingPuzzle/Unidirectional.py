import time
from Puzzle import Puzzle

# Sample boards for 15-sliding Puzzle
board =  ['1','2','3','4',
          '5','6','7','8',
          '_','9','c','f',
          'd','b','a','e']

goal = ['1','2','3','4',
        '5','6','7','8',
        '9','a','b','c',
        'd','e','f','_']


######################### BREADTH FIRST SEARCH ############################
# BFS Search
# Blind search
class bfsSearch:
    def __init__(self, board, goal):
        self.node = Puzzle(board, goal, 0)
        self.closed = []
        self.open = []
        self.dim = 16
        self.goal = goal

    # Checking if board node is equal to goal node
    def CheckBoard(self, Board):
        for i in range(self.dim):
            if Board.board[i] != self.goal[i]:
                return False
        return True

    def Solve(self):
        self.open.append(self.node)  # putting the node into
        moves = 0

        while len(self.open) > 0:
            self.node = self.open[0]
            temp = self.node.getNextBoards()

            if self.CheckBoard(self.node):
                return moves, self.closed

            for boards in temp:
                if boards not in self.closed:
                    self.open.append(boards)

            self.open.remove(self.node)
            self.closed.append(self.node)
            moves = moves + 1

        return False

bfs = bfsSearch(board,goal)
if bfs.Solve():
  move, close = bfs.Solve()
  print("Solution found at level = ",close[len(close)-1].level)
  print("Iterations =", move)
else:
    print("Failed")
t1 = time.time()
print("Execution Time = ", t1-t0)



################################ BEST FIRST SEARCH ##################################

# Best First Search
class BestSearch:
    def __init__(self, board, goal):
        self.node = Puzzle(board, goal, 0)
        self.closed = []
        self.open = []
        self.goal = goal
        self.dim = 16

    # function returning f-value, which in this case is fval = hval
    def fval(self, Board):
        return self.get_manhattan(
            Board.board)  # As best first search only cares about next least cost node, not the previous states

    # function for checking if given node is same as the goal node or not
    def CheckBoard(self):
        for i in range(self.dim):
            if self.node.board[i] != self.goal[i]:
                return False
        return True

    # function to compute our h-value
    def get_manhattan(self, board):
        self.man = 0
        for i in range(self.dim):
            ele = board[i]
            gi = int(i / 4)
            gj = int(i % 4)
            if ele != self.goal[i]:
                ind = self.goal.index(ele)
                co = int(ind % 4)
                ro = int(ind / 4)
                self.man = self.man + abs(gj - co) + abs(gi - ro)
        return self.man

    # function for solving the given board
    def Solve(self):
        self.open.append(self.node)  # storing the node in the open list
        self.node.f_val = self.fval(self.node)  # getting the f-value of the node
        moves = 0  # just for iterations
        while (not self.CheckBoard()):  # if not goal node
            self.node = self.open[0]
            tempBoards = self.node.getNextBoards()  # compute expanded nodes
            for boards in tempBoards:
                self.open.append(boards)
                boards.f_val = self.fval(boards)  # computing f-value for all newly generated nodes
            self.open.remove(self.node)
            self.closed.append(self.node)

            # sorting the open list based on f-value
            self.open = sorted(self.open, key=lambda x: x.f_val, reverse=False)

            moves = moves + 1
        return moves, self.closed

t0 =time.time()
puz = BestSearch(board,goal) # Best FIrst Search
move, closed = puz.Solve() # Solving the puzzle
t1 = time.time()
print("Solution found at level = ", closed[len(closed)-1].level)
print("Iterations = ",move)
print("Execution Time = ", t1-t0)


######################################### A STAR SEARCH #############################################


# A* Search
class ASearch:
    def __init__(self, board, goal):
        self.node = Puzzle(board, goal, 0)  # initializing the search with start state in the board
        self.closed = []  # initializing the closed list, that is, nodes that have been explored and expanded
        self.open = []  # initializing the open list, that is, the nodes which are yet to be explored are kept here
        self.goal = goal  # defining the goal state
        self.dim = 16

    # function for fvalue = gvalue + hvalue, gvalue is nothing but level at which the board was put in the open list
    def fval(self, Board):
        return self.get_manhattan(Board.board) + Board.level

    # function for checking if the board reached is equal to the goal state or not
    def CheckBoard(self):
        for i in range(self.dim):
            if self.node.board[i] != self.goal[i]:
                return False
        return True

    # function to get the hvalue, our heuristic for 15 sliding is Manhattan distance
    def get_manhattan(self, board):
        self.man = 0
        for i in range(self.dim):
            ele = board[i]
            gi = int(i / 4)
            gj = int(i % 4)
            if ele != self.goal[i]:
                ind = self.goal.index(ele)
                co = int(ind % 4)
                ro = int(ind / 4)
                self.man = self.man + abs(gj - co) + abs(gi - ro)
        return self.man

    # function for solving the problem with A* algorithm
    def Solve(self):
        self.open.append(self.node)  # we put the node in the open list, as it is yet to be explored
        self.node.f_val = self.fval(self.node)  # we compute the fval of that node
        moves = 0  # just for computing number of iterations
        while (not self.CheckBoard()):
            self.node = self.open[0]
            tempBoards = self.node.getNextBoards()  # getting next boards, that is, boards created after legal moves were applied
            for boards in tempBoards:
                self.open.append(boards)
                boards.f_val = self.fval(boards)  # computing f-value for each board
            self.open.remove(self.node)  # removing the explored node from the open list
            self.closed.append(self.node)  # putting the explored node in to the closed list

            # sorting the open list based on the value, as we try to expand node with the least f-value
            self.open = sorted(self.open, key=lambda x: x.f_val, reverse=False)

            moves = moves + 1
        return moves, self.closed

t0 =time.time()
puz = ASearch(board,goal)
move, closed = puz.Solve()
t1 = time.time()
print("Solution found at level = ", closed[len(closed)-1].level)
print("Iterations = ",move)
print("Execution Time = ", t1-t0)