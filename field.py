__author__ = 'luoxiang03'

from cell import *


class Field(QWidget):
    def __init__(self, row=20, col=20, cell_size=20, cell_margin=1):
        super(Field, self).__init__()
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.cell_margin = cell_margin
        self.cell = [[0 for col in xrange(self.col)] for row in xrange(self.row)]

        self.place_cell()

        width = self.col * self.cell_size + (self.col - 1) * self.cell_margin
        height = self.row * self.cell_size + (self.row - 1) * self.cell_margin
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

    def place_cell(self):
        index = 0
        layout = QGridLayout()
        layout.setSpacing(self.cell_margin)
        for row in xrange(0, self.row):
            for col in xrange(0, self.col):
                index += 1
                if self.row * 0.25 <= row < self.row * 0.75 and self.col * 0.25 <= col < self.col * 0.75:
                    status = Cell.live
                else:
                    status = Cell.dead
                cell = Cell(index, self.cell_size, status)
                layout.addWidget(cell, row, col)

        self.setLayout(layout)