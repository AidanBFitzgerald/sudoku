import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
x = 0
y = 0
dif = SCREEN_WIDTH / 9


class Board:
    board = [
        [0, 3, 1, 0, 5, 0, 0, 0, 4],
        [0, 0, 0, 7, 0, 0, 0, 0, 1],
        [0, 0, 0, 2, 0, 0, 0, 0, 5],
        [0, 2, 4, 0, 0, 6, 0, 0, 9],
        [0, 8, 0, 0, 0, 0, 0, 5, 0],
        [5, 0, 0, 0, 2, 0, 7, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 2, 0],
        [6, 0, 0, 4, 0, 7, 0, 0, 0]
    ]

    def solve(self):
        empty = find_empty(self.board)
        if not empty:
            return True
        row, col = empty

        for i in range(1, 10):
            if check_valid(self.board, i, [row, col]):
                self.board[row][col] = i
                if self.solve():
                    return True

                self.board[row][col] = 0

        return False


class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col

    def set_value(self, val):
        self.value = val

    def set_temp(self, tmp):
        self.temp = tmp


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return [i, j]  # Row, Col


def check_valid(board, num, pos):
    # Check row
    row = board[pos[0]]
    for i in range(len(row)):
        if num == row[i] and i != pos[1]:
            return False

    # Check column
    for j in range(len(board)):
        if num == board[j][pos[1]] and j != pos[0]:
            return False

    # Check box
    row = pos[0] // 3 * 3
    col = pos[1] // 3 * 3

    for i in range(3):
        for j in range(3):
            if board[row + i][col + j] == num and (row + i != pos[0] or col + j != pos[1]):
                return False
    # Number is valid
    return True


def main():
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Game")

    board = Board()


def get_cords(pos):
    global x, y
    x = pos[0] // dif
    y = pos[1] // dif


board = Board()
for i in range(9):
    print(board.board[i])
board.solve()
print()
for i in range(9):
    print(board.board[i])
