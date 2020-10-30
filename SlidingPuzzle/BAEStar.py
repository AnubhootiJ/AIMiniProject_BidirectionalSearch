import math
from Puzzle import Puzzle
import time

board = ['1','2','3','4',
         '5','6','7','8',
         '_','9','c','f',
         'd','b','a','e']

goal = ['1','2','3','4',
        '5','6','7','8',
        '9','a','b','c',
        'd','e','f','_']


# BAE* Search
class BAESearch:
    def __init__(self, board, goal):
        self.front = Puzzle(board, goal, 0)
        self.rear = Puzzle(goal, board, 0)
        self.closedFront = []
        self.openFront = []
        self.closedRear = []
        self.openRear = []
        self.dim = 16
        self.h0 = self.get_manhattan(board, goal)

    def fval(self, Board):
        return self.get_manhattan(Board.board, Board.goal) + Board.level

    def get_total_error(self, Board):
        return 2 * Board.level + self.get_manhattan(Board.goal, Board.board) - self.get_manhattan(board,
                                                                                                  Board.board) - self.h0

    def CheckBoard(self):
        if len(self.closedFront) == 0 or len(self.closedRear) == 0:
            return False
        else:
            for front in self.closedFront:
                for rear in self.closedRear:
                    if front.board == rear.board:
                        return True, rear.error
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

    def Checkit(self, board1, boards):
        for board2 in boards:
            if board2.board == board1.board:
                return True
        return False

    def Solve(self):
        self.openFront.append(self.front)
        self.openRear.append(self.rear)
        moves = 0
        Lmin = math.inf
        while self.openFront or self.openRear:
            moves = moves + 1
            self.front = self.openFront[0]
            self.rear = self.openRear[0]

            self.closedFront.append(self.front)
            self.closedRear.append(self.rear)

            if self.Checkit(self.front, self.openRear) and Lmin > self.front.error + self.rear.error:
                error_back = self.Checkit(self.front, self.openRear)
                Lmin = self.front.error + error_back
                getmin = min(self.openRear, key=lambda x: x.error)
                Omin = self.front.error + getmin.error
                if Lmin <= Omin:
                    sol_cost = self.h0 + Lmin / 2
                    return sol_cost, moves, self.front
            tempFront = self.front.getNextBoards()
            for boardFront in tempFront:
                if boardFront in self.openFront or boardFront in self.closedFront:
                    if boardFront.error > self.get_total_error(boardFront):
                        boardFront.error = self.get_total_error(boardFront)
                elif boardFront not in self.closedFront:
                    boardFront.error = self.get_total_error(boardFront)
                    self.openFront.append(boardFront)

            if self.Checkit(self.rear, self.openFront) and Lmin > self.rear.error + self.front.error:
                error_front = self.Checkit(self.rear, self.openFront)
                Lmin = self.rear.error + error_front
                getmin = min(self.openFront, key=lambda x: x.error)
                Omin = self.rear.error + getmin.error
                if Lmin <= Omin:
                    sol_cost = self.h0 + Lmin / 2
                    return sol_cost, moves, self.rear
            tempRear = self.rear.getNextBoards()
            for boardRear in tempRear:
                if boardRear in self.openRear or boardRear in self.closedRear:
                    if boardRear.error > self.get_total_error(boardRear):
                        boardRear.error = self.get_total_error(boardRear)
                elif boardRear not in self.closedRear:
                    boardRear.error = self.get_total_error(boardRear)
                    self.openRear.append(boardRear)

            self.openFront.remove(self.front)
            self.openRear.remove(self.rear)

            self.openFront = sorted(self.openFront, key=lambda x: x.error, reverse=False)
            self.openRear = sorted(self.openRear, key=lambda x: x.error, reverse=False)


t0 =time.time()
bi = BAESearch(board,goal)
cost, move, Mid = bi.Solve()
t1 = time.time()
print("Intersection at level = ", Mid.level)
print("Iterations = ",move)
print("Solution Cost = ", cost)
print("Execution Time = ", t1-t0)