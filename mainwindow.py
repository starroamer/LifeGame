__author__ = 'luoxiang03'
#encoding:utf-8

import sys
from field import *


class MainWindow(QWidget):
    timer_interval = 1000

    def __init__(self):
        super(MainWindow, self).__init__()
        self.world_timer = QTimer()
        self.world_timer.timeout.connect(self.new_round)

        self.field = Field()
        self.init_ui()

    def init_ui(self):
        top_layout = QHBoxLayout()

        top_layout.addWidget(self.field)

        self.play_btn = QPushButton(u"开始", self)
        self.play_btn.clicked.connect(self.press_play)
        acc_btn = QPushButton(u"加速", self)
        acc_btn.clicked.connect(self.accelerate)
        deacc_btn = QPushButton(u"减速", self)
        deacc_btn.clicked.connect(self.deaccelerate)
        clear_btn = QPushButton(u"清空", self)
        clear_btn.clicked.connect(self.clear_field)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(deacc_btn)
        bottom_layout.addWidget(self.play_btn)
        bottom_layout.addWidget(acc_btn)
        bottom_layout.addWidget(clear_btn)
        bottom_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("Draw")

        self.resize(self.field.size().width(), self.field.size().height())
        self.center()

        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

    def press_play(self):
        if not self.world_timer.isActive():
            self.world_timer.start(self.timer_interval)
            self.play_btn.setText(u"暂停")
            self.play_btn.repaint()
        else:
            self.world_timer.stop()
            self.play_btn.setText(u"开始")
            self.play_btn.repaint()

    def accelerate(self):
        self.timer_interval /= 2.0
        self.world_timer.start(self.timer_interval)

    def deaccelerate(self):
        self.timer_interval *= 2.0
        self.world_timer.start(self.timer_interval)

    def clear_field(self):
        self.field.clear_field()
        self.world_timer.stop()
        self.play_btn.setText(u"开始")
        self.play_btn.repaint()

    def new_round(self):
        #self.field.reverse_all_cell()
        self.field.start_next_iteration()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()