__author__ = 'luoxiang03'

import sys
from field import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        top_layout = QHBoxLayout()

        field = Field()
        top_layout.addWidget(field)

        play_btn = QPushButton("Play", self)
        stop_btn = QPushButton("Stop", self)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(play_btn)
        bottom_layout.addWidget(stop_btn)
        bottom_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("Draw")

        self.resize(field.size().width(), field.size().height())
        self.center()

        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

    #def paintEvent(self, event):
    #    self.painter.begin(self)
    #    self.draw_cell()
    #    self.painter.end()

    def place_cell(self, layout, field_row, field_col, cell_size, painter):
        index = 0
        geometry = self.geometry()
        start_x = (geometry.width() - field_row * cell_size) / 2
        start_y = (geometry.height() - field_col * cell_size) / 2
        for row in xrange(0, field_row):
            for col in xrange(0, field_col):
                index += 1
                x = start_x + col * cell_size
                y = start_y + row * cell_size
                if field_row * 0.25 <= row < field_row * 0.75 and field_col * 0.25 <= col < field_col * 0.75:
                    color = QColor(Qt.green)
                else:
                    color = QColor(Qt.gray)
                cell = Cell(index, x, y, cell_size, painter, color)
                layout.addWidget(cell, row, col)
                self.cell[row][col] = cell

    #def draw_cell(self):
    #    for col in xrange(self.col):
    #        for row in xrange(self.row):
    #            self.cell[row][col].draw()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()