__author__ = 'luoxiang03'

import random
from cell import *


class Field(QWidget):
    random_live_prob = 0.3

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

        #cells which status will be changed
        self.status_change_cell = []

        #cells which status may be changed and need to be calculated
        #include live cell and it's neighbors
        self.consider_cell = {}

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
                #if random.random() < Field.random_live_prob:
                #    status = Cell.live
                #else:
                #    status = Cell.dead
                cell = Cell(self, self.cell_size, Cell.dead,
                            self.cell_reproduce_factor,
                            self.cell_under_population_threshold,
                            self.cell_overcrowding_threshold)
                cell.setObjectName("cell-%s-%s" % (row_index, col_index))
                self.set_cell_neighbor(cell, row_index, col_index)
                self.cell_matrix[row_index][col_index] = cell
                layout.addWidget(cell, row_index, col_index)

        self.setLayout(layout)

    def reverse_all_cell(self):
        for row_index in xrange(0, self.row):
            for col_index in xrange(0, self.col):
                cur_cell = self.cell_matrix[row_index][col_index]
                cur_cell.reverse()
                cur_cell.repaint()

    def execute_change(self):
        if self.status_change_cell:
            for cell in self.status_change_cell:
                cell.reverse()
                cell.repaint()
            del self.status_change_cell[:]

    def start_next_iteration(self):
        self.scan_cell_for_next_iteration()
        self.execute_change()

    def scan_cell_for_next_iteration(self):
        for cell in self.consider_cell:
            self.calculate_cell_next_status(cell)

    def calculate_cell_next_status(self, cell):
        cell_status = cell.get_status()
        change_status = False
        live_neighbor_num = cell.get_live_neighbor_num()

        #cell living strategy

        #in case below, change status of cell
        #otherwise, stay next status of cell
        if cell_status == Cell.dead and live_neighbor_num == cell.reproduce_factor:
            change_status = True
        elif cell_status == Cell.live:
            if live_neighbor_num < cell.under_population_threshold:
                change_status = True
            elif live_neighbor_num > cell.overcrowding_threshold:
                change_status = True

        if change_status:
            self.status_change_cell.append(cell)

    def clear_field(self):
        repaint_flag = False
        for row_index in xrange(self.row):
            for col_index in xrange(self.col):
                cur_cell = self.cell_matrix[row_index][col_index]
                if cur_cell.get_status() == Cell.live:
                    repaint_flag = True
                    cur_cell.set_status(Cell.dead)
                cur_cell.clear_live_neighbor_num()

                if repaint_flag:
                    cur_cell.repaint()
        del self.status_change_cell[:]
        self.consider_cell.clear()

    def random_gen_cell(self):
        self.clear_field()
        cell_num = int(self.row * self.col * self.random_live_prob)
        print cell_num
        for i in xrange(cell_num):
            row_index = random.randint(0, self.row - 1)
            col_index = random.randint(0, self.col - 1)
            cell = self.cell_matrix[row_index][col_index]
            cell.reverse()
            cell.repaint()