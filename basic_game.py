import copy

import pygame

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 540
BUTTON_BAR_HEIGHT = 40
x = 0
y = 0
dif = SCREEN_WIDTH / 9
wrong_answer_count = 0
FPS = 10
BACKGROUND_COLOUR = (255, 255, 255)
LINE_COLOUR_LIGHT = (200, 200, 200)
BLACK = (0, 0, 0)
BOX_SIZE = SCREEN_WIDTH // 3
SQUARE_SIZE = BOX_SIZE // 3
NUMBER_SIZE = SQUARE_SIZE // 3
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SCREEN = BASIC_FONT = BASIC_FONT_SIZE = WRONG_FONT = None

BOARD = [
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


class Square:
    """Represents single square of a Sudoku board"""
    rows = 9
    cols = 9

    def __init__(self, value, row, col):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.valid = False

    def set_value(self, val):
        self.value = val

    def set_temp(self, tmp):
        self.temp = tmp

    def is_empty(self):
        if self.value == 0:
            return True
        return False

    def get_pos(self):
        return [self.row, self.col]

    def __repr__(self):
        return str(self.value)


def init_squares(board):
    """Converts board from list of numbers to list of square objects"""
    squares_list = []
    for y_pos in range(0, 9):
        temp_list = []
        for x_pos in range(0, 9):
            s = Square(board[y_pos][x_pos], x_pos, y_pos)
            if board[y_pos][x_pos] != 0:
                s.valid = True
            temp_list.append(s)
        squares_list.append(temp_list)

    return squares_list


def solve(board):
    """Solve Sudoku board using recursive backtracking algorithm"""
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for i in range(1, 10):
        if check_valid(board, i, [row, col]):
            board[row][col].value = i
            board[row][col].valid = True
            if solve(board):
                return True

            board[row][col].value = 0

    return False


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].value == 0:
                return [i, j]  # Row, Col


def check_valid(board, num, pos):
    # Check row
    row = board[pos[0]]
    for i in range(len(row)):
        if num == row[i].value and i != pos[1]:
            return False

    # Check column
    for j in range(len(board)):
        if num == board[j][pos[1]].value and j != pos[0]:
            return False

    # Check box
    row = pos[0] // 3 * 3
    col = pos[1] // 3 * 3

    for i in range(3):
        for j in range(3):
            if board[row + i][col + j].value == num and (row + i != pos[0] or col + j != pos[1]):
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
    for i in range(0, SCREEN_WIDTH + 1, BOX_SIZE):  # Draw vertical lines
        pygame.draw.line(SCREEN, BLACK, (i, 0), (i, SCREEN_HEIGHT))
    for i in range(0, SCREEN_HEIGHT + 1, BOX_SIZE):  # Draw horizontal lines
        pygame.draw.line(SCREEN, BLACK, (0, i), (SCREEN_WIDTH, i))


def display_board(board):
    for row in board:
        for square in row:
            if square.value != 0:
                pos = square.get_pos()
                x_pos = int(pos[0] * SQUARE_SIZE + SQUARE_SIZE / 2)
                y_pos = int(pos[1] * SQUARE_SIZE + SQUARE_SIZE / 2)
                if square.valid:
                    cell_surf = BASIC_FONT.render('%s' % square.value, True, BLACK)
                else:
                    cell_surf = BASIC_FONT.render('%s' % square.value, True, RED)
                cell_rect = cell_surf.get_rect()
                cell_rect.center = (x_pos, y_pos)
                SCREEN.blit(cell_surf, cell_rect)


def draw_selected(x_click, y_click):
    x_pos, y_pos = get_cords([x_click, y_click])
    x_pos = int(x_pos * SQUARE_SIZE)
    y_pos = int(y_pos * SQUARE_SIZE)
    pygame.draw.rect(SCREEN, BLUE, (x_pos, y_pos, SQUARE_SIZE, SQUARE_SIZE), 1)


def display_wrong_answers():
    wrong_font = pygame.font.Font('freesansbold.ttf', 10)
    wrong_answer_text = wrong_font.render('Wrong answers: %s' % wrong_answer_count, True, BLACK)
    wrong_text_frame = wrong_answer_text.get_rect()
    wrong_text_frame.center = (SCREEN_WIDTH - 50, SCREEN_HEIGHT + 20)
    SCREEN.blit(wrong_answer_text, wrong_text_frame)


def get_cords(pos):
    x_pos = int(pos[0] // dif)
    y_pos = int(pos[1] // dif)
    return [x_pos, y_pos]


def change_num(board, solved_board, x_click, y_click, num):
    global wrong_answer_count
    x_pos, y_pos = get_cords([x_click, y_click])
    if board[y_pos][x_pos].value == 0 or not board[y_pos][x_pos].valid:  # Check if number has been entered or if
        # number is not valid
        board[y_pos][x_pos].value = num
        if board[y_pos][x_pos].value == solved_board[y_pos][x_pos].value:
            board[y_pos][x_pos].valid = True
        else:
            wrong_answer_count += 1


def main():
    global SCREEN, x, y
    # Initialize pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # create the screen
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BUTTON_BAR_HEIGHT))

    # Title and Icon
    pygame.display.set_caption("Sudoku Solver")
    icon = pygame.image.load('assets/sudoku_logo.png')
    pygame.display.set_icon(icon)

    global BASIC_FONT, BASIC_FONT_SIZE, WRONG_FONT
    BASIC_FONT_SIZE = 40
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    # Solve button
    font = pygame.font.Font('freesansbold.ttf', 20)
    button_text = font.render('Solve', True, BLACK)
    text_frame = button_text.get_rect()
    text_frame.center = (20 + 40 ,SCREEN_HEIGHT + 20)
    button = pygame.Rect(20, SCREEN_HEIGHT + 5, 80, 30)

    # Initializing board
    board = init_squares(BOARD)

    # Solve Board
    board_solved = copy.deepcopy(board)
    solve(board_solved)

    # Game loop
    running = True
    mouseClicked = False
    x_click = 0
    y_click = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # mouse movement commands
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos

            # Mouse click commands
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if button.collidepoint(mouse_pos):
                    board = board_solved
                elif y <= SCREEN_HEIGHT:
                    x, y = event.pos
                    mouseClicked = True
                    x_click = x
                    y_click = y
            # Key pressed down
            elif event.type == pygame.KEYDOWN:
                if event.unicode >= '0' and event.unicode <= '9':
                    num = int(event.unicode)
                    change_num(board, board_solved, x_click, y_click, num)

        SCREEN.fill(BACKGROUND_COLOUR)
        draw_grid()
        if mouseClicked:
            draw_selected(x_click, y_click)
        SCREEN.blit(button_text, text_frame)
        pygame.draw.rect(SCREEN, BLACK, button, 3)
        display_wrong_answers()
        display_board(board)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
