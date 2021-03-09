import pygame

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 450
x = 0
y = 0
dif = SCREEN_WIDTH / 9
FPS = 10
BACKGROUND_COLOUR = (255, 255, 255)
LINE_COLOUR_LIGHT = (200, 200, 200)
LINE_COLOUR_DARK = (0, 0, 0)
BOX_SIZE = SCREEN_WIDTH // 3
SQUARE_SIZE = BOX_SIZE // 3


class Board:
    """Class board:
        Contains Sudoku board that needs to be solved and solves board"""
    board = [
        [0, 0, 0, 0, 9, 0, 0, 3, 0],
        [0, 0, 5, 0, 0, 6, 0, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 0, 8],
        [0, 0, 2, 0, 0, 0, 5, 0, 0],
        [8, 0, 0, 0, 7, 0, 0, 0, 1],
        [0, 0, 4, 0, 0, 0, 6, 0, 0],
        [9, 0, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 5, 0, 0, 2, 0, 0],
        [0, 7, 0, 0, 1, 0, 0, 0, 0]
    ]

    def solve(self):
        """Solve Sudoku board using recursive backtracking algorithm"""
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
    """Represents single square of a Sudoku board"""
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


def draw_grid():
    # Draw light lines
    for i in range(0, SCREEN_WIDTH, SQUARE_SIZE):  # Draw vertical lines
        pygame.draw.line(SCREEN, LINE_COLOUR_LIGHT, (i, 0), (i, SCREEN_HEIGHT))
    for i in range(0, SCREEN_HEIGHT, SQUARE_SIZE):  # Draw horizontal lines
        pygame.draw.line(SCREEN, LINE_COLOUR_LIGHT, (0, i), (SCREEN_WIDTH, i))

    # Draw dark lines
    for i in range(0, SCREEN_WIDTH, BOX_SIZE): # Draw vertical lines
        pygame.draw.line(SCREEN, LINE_COLOUR_DARK, (i, 0), (i, SCREEN_HEIGHT))
    for i in range(0, SCREEN_HEIGHT, BOX_SIZE): # Draw horizontal lines
        pygame.draw.line(SCREEN, LINE_COLOUR_DARK, (0, i), (SCREEN_WIDTH, i))


def get_cords(pos):
    global x, y
    x = pos[0] // dif
    y = pos[1] // dif


def main():
    global SCREEN
    # Initialize pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # create the screen
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Title and Icon
    pygame.display.set_caption("Sudoku Solver")
    icon = pygame.image.load('assets/sudoku_logo.png')
    pygame.display.set_icon(icon)

    # Game loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill(BACKGROUND_COLOUR)
        draw_grid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# board = Board()
# # prints unsolved board
# for i in range(9):
#     print(board.board[i])
# board.solve()
#
# print()
# # prints solved board
# for i in range(9):
#     print(board.board[i])

if __name__ == '__main__':
    main()
