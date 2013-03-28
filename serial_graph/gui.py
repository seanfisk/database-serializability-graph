#!/usr/bin/env python
""":mod:`serial_graph.gui` -- Graphical interface
"""

import sys
from cStringIO import StringIO

from PySide import QtCore, QtGui, QtSvg

from serial_graph.graph import generate_serializability_graph


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.central_widget = QtGui.QWidget()
        self.central_layout = QtGui.QHBoxLayout(self.central_widget)

        self.form_layout = QtGui.QVBoxLayout()
        self.input_area = QtGui.QPlainTextEdit()
        self.form_layout.addWidget(self.input_area)
        self.submit_button = QtGui.QPushButton('Submit')
        self.submit_button.clicked.connect(self._submit_button_clicked)
        self.form_layout.addWidget(self.submit_button)
        self.central_layout.addLayout(self.form_layout)

        self.output_area = QtSvg.QSvgWidget()
        self.central_layout.addWidget(self.output_area)

        self.setCentralWidget(self.central_widget)

    def _submit_button_clicked(self):
        schedule_file = StringIO(self.input_area.toPlainText())
        graph = generate_serializability_graph(schedule_file)
        schedule_file.close()

        output_svg_file = StringIO()
        graph.draw(output_svg_file, format='svg')
        self.output_area.load(QtCore.QByteArray(output_svg_file.getvalue()))
        output_svg_file.close()


def main(argv):
    app = QtGui.QApplication(argv)

    win = MainWindow()
    win.show()
    win.raise_()

    app.exec_()
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
