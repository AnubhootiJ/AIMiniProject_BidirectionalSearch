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


################## BI-DIRECTIONAL BREADTH FIRST SEARCH ##############################

# Bi-diretional BFS Search
# Blind Search, can take a lot of time to come to a solution
class BiBFSSearch:
    def __init__(self, board, goal):
        self.front = Puzzle(board, goal, 0)
        self.rear = Puzzle(goal, board, 0)
        self.closedFront = []
        self.openFront = []
        self.closedRear = []
        self.openRear = []
        self.dim = 16

    def CheckBoard(self):
        if len(self.closedFront) == 0 or len(self.closedRear) == 0:
            return False
        else:
            for front in self.closedFront:
                for rear in self.closedRear:
                    if front.board == rear.board:
                        return True
        return False

    def Solve(self):  # no fvalue here, as this is a blind search.
        # we run two blind searches in parallel, one from start node and another from goal node
        self.openFront.append(self.front)
        self.openRear.append(self.rear)
        moves = 0
        while (not self.CheckBoard()):
            if len(self.openFront) != 0:

                self.front = self.openFront[0]
                tempFront = self.front.getNextBoards()

                for boardFront in tempFront:
                    if boardFront not in self.closedFront:
                        self.openFront.append(boardFront)
                self.openFront.remove(self.front)
                self.closedFront.append(self.front)

            if len(self.openRear) != 0:
                self.rear = self.openRear[0]
                tempRear = self.rear.getNextBoards()

                for boards in tempRear:
                    if boards not in self.closedRear:
                        self.openRear.append(boards)
                self.openRear.remove(self.rear)
                self.closedRear.append(self.rear)
            moves = moves + 1
        return moves, self.closedFront, self.closedRear

t0 =time.time()
bfs = BiBFSSearch(board,goal)
move, front, rear = bfs.Solve()
t1 = time.time()
print("Intersection at level = ", front[len(front)-1].level)
print("Iterations = ",move)
print("Execution Time = ", t1-t0)



########################### BI-DIRECTIONAL BEST FIRST SEARCH ######################################

# Bi-diretional Best First Search
class BiBestSearch:
    def __init__(self, board, goal):
        self.front = Puzzle(board, goal, 0)
        self.rear = Puzzle(goal, board, 0)
        self.closedFront = []
        self.openFront = []
        self.closedRear = []
        self.openRear = []
        self.dim = 16

    def fval(self, Board):
        return self.get_manhattan(Board.board, Board.goal)

    def CheckBoard(self):
        if len(self.closedFront) == 0 or len(self.closedRear) == 0:
            return False
        else:
            for front in self.closedFront:
                for rear in self.closedRear:
                    if front.board == rear.board:
                        return True
        return False

    def get_manhattan(self, board, Tgoal):
        self.man = 0
        for i in range(self.dim):
            ele = board[i]
            gi = int(i / 4)
            gj = int(i % 4)
            if ele != Tgoal[i]:
                ind = Tgoal.index(ele)
                co = int(ind % 4)
                ro = int(ind / 4)
                self.man = self.man + abs(gj - co) + abs(gi - ro)
        return self.man

    def Solve(self):  # same as bi-dirc A* but we have fvalue = hvalue here.
        self.openFront.append(self.front)
        self.openRear.append(self.rear)
        self.front.f_val = self.fval(self.front)
        self.rear.f_val = self.fval(self.rear)
        moves = 0
        while (not self.CheckBoard()):
            # Forward Search
            if len(self.openFront) != 0:

                self.front = self.openFront[0]
                tempFront = self.front.getNextBoards()

                for boardFront in tempFront:
                    if boardFront not in self.closedFront:
                        boardFront.f_val = self.fval(boardFront)
                        self.openFront.append(boardFront)
                self.openFront.remove(self.front)
                self.closedFront.append(self.front)

                # Backward Search
            if len(self.openRear) != 0:
                self.rear = self.openRear[0]
                tempRear = self.rear.getNextBoards()

                for boards in tempRear:
                    if boards not in self.closedRear:
                        boards.f_val = self.fval(boards)
                        self.openRear.append(boards)
                self.openRear.remove(self.rear)
                self.closedRear.append(self.rear)

                # sorting open list of both the searches
            self.openFront = sorted(self.openFront, key=lambda x: x.f_val, reverse=False)
            self.openRear = sorted(self.openRear, key=lambda x: x.f_val, reverse=False)

            moves = moves + 1
        return moves, self.closedFront, self.closedRear

t0 =time.time()
bi = BiBestSearch(board,goal)
move, front, rear = bi.Solve()
t1 = time.time()
print("Intersection at level = ", front[len(front)-1].level)
print("Iterations = ",move)
print("Execution Time = ", t1-t0)


##################################### BI-DIRECTIONAL A STAR SEARCH ####################################

# Bi-diretional A* Search
class BiSearch:
    def __init__(self, board, goal):
        self.front = Puzzle(board, goal, 0)
        self.rear = Puzzle(goal, board, 0)
        self.closedFront = []
        self.openFront = []
        self.closedRear = []
        self.openRear = []
        self.dim = 16

    def fval(self, Board):
        return self.get_manhattan(Board.board, Board.goal) + Board.level

    # function to check if there is a common board in the closed list of both the searches
    def CheckBoard(self):
        if len(self.closedFront) == 0 or len(self.closedRear) == 0:
            return False
        else:
            for front in self.closedFront:
                for rear in self.closedRear:
                    if front.board == rear.board:
                        return True
        return False

    def get_manhattan(self, board, Tgoal):
        self.man = 0
        for i in range(self.dim):
            ele = board[i]
            gi = int(i / 4)
            gj = int(i % 4)
            if ele != Tgoal[i]:
                ind = Tgoal.index(ele)
                co = int(ind % 4)
                ro = int(ind / 4)
                self.man = self.man + abs(gj - co) + abs(gi - ro)
        return self.man

    def Solve(self):
        self.openFront.append(self.front)
        self.openRear.append(self.rear)
        self.front.f_val = self.fval(self.front)
        self.rear.f_val = self.fval(self.rear)
        moves = 0
        while (
        not self.CheckBoard()):  # we have two searches running in parallel, we stop as soon as there is a common board in the lcosed list of both the searches

            # Forward Search
            if len(self.openFront) != 0:

                self.front = self.openFront[0]
                tempFront = self.front.getNextBoards()

                for boardFront in tempFront:
                    if boardFront not in self.closedFront:
                        boardFront.f_val = self.fval(boardFront)
                        self.openFront.append(boardFront)
                self.openFront.remove(self.front)
                self.closedFront.append(self.front)

                # Backward Search
            if len(self.openRear) != 0:
                self.rear = self.openRear[0]
                tempRear = self.rear.getNextBoards()

                for boards in tempRear:
                    if boards not in self.closedRear:
                        boards.f_val = self.fval(boards)
                        self.openRear.append(boards)
                self.openRear.remove(self.rear)
                self.closedRear.append(self.rear)

            self.openFront = sorted(self.openFront, key=lambda x: x.f_val, reverse=False)
            self.openRear = sorted(self.openRear, key=lambda x: x.f_val, reverse=False)

            moves = moves + 1
        return moves, self.closedFront, self.closedRear

t0 =time.time()
bi = BiSearch(board,goal)
move, front, rear = bi.Solve()
t1 = time.time()
print("Intersection at level = ", front[len(front)-1].level)
print("Iterations = ",move)
print("Execution Time = ", t1-t0)