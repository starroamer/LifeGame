__author__ = 'luoxiang03'

from cell import *


class Field(QWidget):
    def __init__(self, row=20, col=20, cell_size=20, cell_margin=1):
        super(Field, self).__init__()
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.cell_margin = cell_margin
        self.cell_matrix = [[0 for col in xrange(self.col)] for row in xrange(self.row)]

        self.place_cell()

        width = self.col * self.cell_size + (self.col - 1) * self.cell_margin
        height = self.row * self.cell_size + (self.row - 1) * self.cell_margin
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

    def set_cell_neighbor(self, cell, cur_row, cur_col):
        if cur_row > 0:
            cell.setneighbor(Cell.top, self.cell_matrix[cur_row - 1][cur_col])
        if cur_row < self.row - 1:
            cell.setneighbor(Cell.bottom, self.cell_matrix[cur_row + 1][cur_col])
        if cur_col > 0:
            cell.setneighbor(Cell.left, self.cell_matrix[cur_row][cur_col - 1])
        if cur_col < self.col - 1:
            cell.setneighbor(Cell.right, self.cell_matrix[cur_row][cur_col + 1])

    def place_cell(self):
        layout = QGridLayout()
        layout.setSpacing(self.cell_margin)
        for row_index in xrange(0, self.row):
            for col_index in xrange(0, self.col):
                if self.row * 0.25 <= row_index < self.row * 0.75 and self.col * 0.25 <= col_index < self.col * 0.75:
                    status = Cell.live
                else:
                    status = Cell.dead
                cell = Cell(self.cell_size, status)
                self.cell_matrix[row_index][col_index] = cell
                layout.addWidget(cell, row_index, col_index)

        self.setLayout(layout)