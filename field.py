__author__ = 'luoxiang03'

import random
from cell import *


class Field(QWidget):
    random_live_prob = 0.15

    def __init__(self, row=20, col=20, cell_size=20, cell_margin=1):
        super(Field, self).__init__()
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.cell_margin = cell_margin
        self.cell_matrix = [[0 for col in xrange(self.col)] for row in xrange(self.row)]
        self.cell_reproduce_factor = 3
        self.cell_under_population_threshold = 2
        self.cell_overcrowding_threshold = 3
        self.next_change_cell = []

        self.place_cell()

        width = self.col * self.cell_size + (self.col - 1) * self.cell_margin
        height = self.row * self.cell_size + (self.row - 1) * self.cell_margin
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

    #set neighbor relationship for current cell and it's existed neighbors
    def set_cell_neighbor(self, cell, cur_row, cur_col):
        if cur_col > 0:
            #set current cell's left neighbor
            #alse set top neighbor's right neighbor to current cell
            left_neighbor = self.cell_matrix[cur_row][cur_col - 1]
            cell.set_neighbor(Cell.left, left_neighbor)
            left_neighbor.set_neighbor(Cell.right, cell)

        if cur_row > 0:
            top_neighbor = self.cell_matrix[cur_row - 1][cur_col]
            cell.set_neighbor(Cell.top, top_neighbor)
            top_neighbor.set_neighbor(Cell.bottom, cell)

            if cur_col > 0:
                top_left_neighbor = self.cell_matrix[cur_row - 1][cur_col - 1]
                cell.set_neighbor(Cell.top_left, top_left_neighbor)
                top_left_neighbor.set_neighbor(Cell.bottom_right, cell)

            if cur_col < self.col - 1:
                top_right_neighbor = self.cell_matrix[cur_row - 1][cur_col + 1]
                cell.set_neighbor(Cell.top_right, top_right_neighbor)
                top_right_neighbor.set_neighbor(Cell.bottom_left, cell)

    def shuffle_cell(self):
        pass

    def place_cell(self):
        layout = QGridLayout()
        layout.setSpacing(self.cell_margin)
        for row_index in xrange(0, self.row):
            for col_index in xrange(0, self.col):
                if random.random() < Field.random_live_prob:
                    status = Cell.live
                else:
                    status = Cell.dead
                cell = Cell(self.cell_size, status,
                            self.cell_reproduce_factor,
                            self.cell_under_population_threshold,
                            self.cell_overcrowding_threshold)
                cell.setObjectName("cell-%s-%s" % (row_index, col_index))
                self.set_cell_neighbor(cell, row_index, col_index)
                self.cell_matrix[row_index][col_index] = cell
                layout.addWidget(cell, row_index, col_index)

        #self.print_all_cell_neighbor()

        self.setLayout(layout)

    def reverse_all_cell(self):
        for row_index in xrange(0, self.row):
            for col_index in xrange(0, self.col):
                cur_cell = self.cell_matrix[row_index][col_index]
                cur_cell.reverse()
                cur_cell.repaint()

    def execute_last_iteration_change(self):
        for cell in self.next_change_cell:
            cell.reverse()
            cell.repaint()
        del self.next_change_cell[:]

    def start_next_iteration(self):
        self.execute_last_iteration_change()
        self.scan_cell_for_next_iteration()

    def scan_cell_for_next_iteration(self):
        for row_index in xrange(0, self.row):
            for col_index in xrange(0, self.col):
                cur_cell = self.cell_matrix[row_index][col_index]
                self.calcu_cell_next_status(cur_cell)

    def calcu_cell_next_status(self, cell):
        live_neighbor_num = 0
        cell_status = cell.get_status()
        change_next_status = False
        for neighbor in cell.get_neighbor_list():
            if neighbor.get_status() == Cell.live:
                live_neighbor_num += 1

        #cell living strategy

        #in case below, change next status of cell
        #otherwise, stay next status of cell
        if cell_status == Cell.dead and live_neighbor_num == cell.reproduce_factor:
            change_next_status = True
        elif cell_status == Cell.live:
            if live_neighbor_num < cell.under_population_threshold:
                change_next_status = True
            elif live_neighbor_num > cell.overcrowding_threshold:
                change_next_status = True

        if change_next_status:
            cell.reverse_next_status()
            self.next_change_cell.append(cell)
        else:
            cell.stay_next_status()