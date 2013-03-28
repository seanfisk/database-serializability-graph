#!/usr/bin/env python

import sys

from PySide import QtGui, QtSvg


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.central_widget = QtGui.QWidget()
        self.central_layout = QtGui.QHBoxLayout(self.central_widget)

        self.input_area = QtGui.QTextEdit()
        self.central_layout.addWidget(self.input_area)

        self.output_area = QtSvg.QSvgWidget('out.svg')
        self.central_layout.addWidget(self.output_area)

        self.setCentralWidget(self.central_widget)


def main(argv):
    app = QtGui.QApplication(argv)

    win = MainWindow()
    win.show()
    win.raise_()

    app.exec_()
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
