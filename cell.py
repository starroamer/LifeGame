__author__ = 'luoxiang03'


from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Cell(QWidget):
    change_signal = pyqtSignal()
    live, dead = range(2)
    dead_color = QColor(Qt.gray)
    live_color = QColor(Qt.darkGreen)
    status_color = {live: live_color, dead: dead_color}
    top, bottom, left, right = range(4)

    def __init__(self, size=10, status=live):
        super(Cell, self).__init__()
        self.cell_size = size

        self.status = status
        self.color = Cell.status_color[status]
        self.neighbor = [None] * 4

        self.change_signal.connect(self.repaint)
        self.resize(size, size)

    def do_draw(self, painter, color):
        painter.fillRect(0, 0, self.cell_size, self.cell_size, color)

        #painter.setPen(color.light())
        #painter.drawLine(0, 0, self.cell_size - 1, 0)
        #painter.drawLine(0, 0, 0, self.cell_size - 1)
        #
        #painter.setPen(color.dark())
        #painter.drawLine(0, self.cell_size - 1, self.cell_size - 1, self.cell_size - 1)
        #painter.drawLine(self.cell_size - 1, 1, self.cell_size - 1, + self.cell_size - 1)

    def reverse(self):
        if self.status == self.dead:
            self.setstatus(self.live)
        elif self.status == self.live:
            self.setstatus(self.dead)

    def draw(self, painter):
        self.do_draw(painter, self.color)

    def setstatus(self, status):
        self.status = status
        self.color = Cell.status_color[self.status]

    def getstatus(self):
        return self.status

    def setneighbor(self, direction, neighbor):
        self.neighbor[direction] = neighbor

    def getneighbor(self, direction):
        return self.neighbor[direction]

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        self.reverse()
        self.change_signal.emit()
