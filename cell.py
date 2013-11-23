__author__ = 'luoxiang03'


from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Cell(QWidget):
    dead, live = range(2)
    dead_color = QColor(Qt.gray)
    live_color = QColor(Qt.darkGreen)
    status_color = {live: live_color, dead: dead_color}

    directions = range(8)
    top_left, top, top_right, left, right, bottom_left, bottom, bottom_right = directions
    directions_name = dict()
    directions_name[top_left] = "top_left"
    directions_name[top] = "top"
    directions_name[top_right] = "top_right"
    directions_name[left] = "left"
    directions_name[right] = "right"
    directions_name[bottom_left] = "bottom_left"
    directions_name[bottom] = "bottom"
    directions_name[bottom_right] = "bottom_right"

    def __init__(self, field, size=10, status=live,
                 reproduce_factor=3,
                 under_population_threshold=2,
                 overcrowding_threshold=3):
        super(Cell, self).__init__()
        self.cell_size = size

        #dead cell become live when live neighbor num equal to reproduce_factor
        self.reproduce_factor = reproduce_factor

        #live cell become dead when live neighbor num less than under_population_threshold
        self.under_population_threshold = under_population_threshold

        #live cell become dead when live neighbor num more than overcrowding_threshold
        self.overcrowding_threshold = overcrowding_threshold

        self.field = field

        self.current_status = status
        self.color = Cell.status_color[status]

        self.neighbor = dict.fromkeys(Cell.directions)
        self.live_neighbor = 0

        self.resize(size, size)

    def do_draw(self, painter, color):
        painter.fillRect(0, 0, self.cell_size, self.cell_size, color)

    def reverse(self):
        neighbor_list = self.get_neighbor_list()
        if self.current_status == self.dead:
            #set cell status to live
            self.set_status(self.live)

            #add live cell and it's neighbors to consider cell list
            self.field.consider_cell[self] = 1
            for cell in neighbor_list:
                cell.add_live_neighbor_num()
                self.field.consider_cell[cell] = 1
        elif self.current_status == self.live:
            #set cell status to dead
            self.set_status(self.dead)

            #if this cell and it's neighbor has no live neighbor, remove it from consider cell list
            if self.get_live_neighbor_num() == 0:
                    del self.field.consider_cell[self]
            for cell in neighbor_list:
                cell.minus_live_neighbor_num()
                if cell.get_live_neighbor_num() == 0 and cell.get_status() == Cell.dead:
                    del self.field.consider_cell[cell]

    def draw(self, painter):
        self.do_draw(painter, self.color)

    def set_status(self, status):
        self.current_status = status
        self.color = Cell.status_color[self.current_status]

    def get_status(self):
        return self.current_status

    def set_neighbor(self, direction, neighbor):
        self.neighbor[direction] = neighbor

    def get_neighbor(self, direction):
        return self.neighbor[direction]

    def get_neighbor_list(self):
        neighbors = [i for i in self.neighbor.values() if i]
        return neighbors

    def add_live_neighbor_num(self):
        self.live_neighbor += 1
        #print "%s live neighbor num = %d" % (self.objectName(), self.live_neighbor)

    def minus_live_neighbor_num(self):
        self.live_neighbor -= 1
        #print "%s live neighbor num = %d" % (self.objectName(), self.live_neighbor)

    def get_live_neighbor_num(self):
        return self.live_neighbor

    def clear_live_neighbor_num(self):
        self.live_neighbor = 0

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        self.reverse()
        self.repaint()
