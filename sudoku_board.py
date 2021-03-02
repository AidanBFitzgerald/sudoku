from random import shuffle
import pygame


class Board:
    def __init__(self):
        self.board_matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.cell_list = random_cells()
        self.populate()

    def next_cell(self):
        if len(self.cell_list) > 0:
            for i in range(len(self.cell_list)):
                cell = self.cell_list[i]
                if self.board_matrix[cell[0]][cell[1]] == 0:
                    return self.cell_list[i]

    def populate(self):
        cell = self.next_cell()
        if cell == self.cell_list[3]:
            print(cell)
        if not cell:
            return True
        for i in range(1, 10):
            if check_valid(self.board_matrix, i, cell):
                self.board_matrix[cell[0]][cell[1]] = i

                if self.populate():
                    return True

                self.board_matrix[cell[0]][cell[1]] = 0

        return False


def random_cells():
    cell_numbers = []
    for i in range(0, 9):
        for j in range(0, 9):
            cell_numbers.append([i, j])
    shuffle(cell_numbers)
    return cell_numbers


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


b = Board()
print(b.board_matrix)
