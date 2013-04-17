#!/usr/bin/env python
""":mod:`serial_graph.gui` -- Graphical interface
"""

from __future__ import division

import sys
from cStringIO import StringIO

from PySide import QtCore, QtGui, QtSvg

from serial_graph.graph import generate_serializability_graph, ParseError

import networkx


class AspectRatioSvgWidget(QtSvg.QSvgWidget):
    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        default_width, default_height = self.renderer().defaultSize().toTuple()
        widget_width, widget_height = self.size().toTuple()
        ratio_x = widget_width / default_width
        ratio_y = widget_height / default_height
        if ratio_x < ratio_y:
            new_width = widget_width
            new_height = widget_width * default_height / default_width
            new_left = 0
            new_top = (widget_height - new_height) / 2
        else:
            new_width = widget_height * default_width / default_height
            new_height = widget_height
            new_left = (widget_width - new_width) / 2
            new_top = 0
        self.renderer().render(
            painter,
            QtCore.QRectF(new_left, new_top, new_width, new_height))


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Create menu.
        self.menu_bar = QtGui.QMenuBar()
        self.file_menu = self.menu_bar.addMenu('&File')
        # self.file_action = self.file_menu.addAction('&Open...')
        # self.file_action.setShortcut(QtGui.QKeySequence.Open)
        # self.file_action.triggered.connect(self._load_file)
        self.submit_action = self.file_menu.addAction('Submit')
        # self.submit_action.setShortcut(QtGui.QKeySequence(
        #     QtCore.Qt.ControlModifier | QtCore.Qt.Key_Return))
        self.submit_action.triggered.connect(self._submit)
        self.quit_action = self.file_menu.addAction('&Quit')
        self.quit_action.setShortcut(QtGui.QKeySequence.Quit)
        self.quit_action.triggered.connect(self.close)
        self.setMenuBar(self.menu_bar)

        # Create central widget.
        self.central_widget = QtGui.QWidget()
        self.central_layout = QtGui.QHBoxLayout(self.central_widget)

        # Left side.
        self.form_layout = QtGui.QVBoxLayout()
        self.input_area = QtGui.QPlainTextEdit()
        font = self.input_area.font()
        font.setPointSize(50)
        self.input_area.setFont(font)
        self.form_layout.addWidget(self.input_area)
        self.submit_button = QtGui.QPushButton('Submit')
        self.submit_button.setShortcut(QtGui.QKeySequence(
            QtCore.Qt.ControlModifier | QtCore.Qt.Key_Return))
        self.submit_button.clicked.connect(self._submit)
        self.form_layout.addWidget(self.submit_button)
        self.central_layout.addLayout(self.form_layout, 1)

        # Right side.
        self.output_layout = QtGui.QVBoxLayout()
        self.output_area = AspectRatioSvgWidget()
        self.output_layout.addWidget(self.output_area, 1)
        self.conflict_serializable_label = QtGui.QLabel()
        self.output_layout.addWidget(
            self.conflict_serializable_label, 0, QtCore.Qt.AlignHCenter)
        self.central_layout.addLayout(self.output_layout, 1)

        self.setCentralWidget(self.central_widget)

        # Load up default data.
        self._load_default_data()
        # self._submit()

    def _load_default_data(self):
        self.input_area.setPlainText('''r1(X)
r2(Z)
r3(X)
r1(Z)
r2(Y)
r3(Y)
w1(X)
w2(Z)
w3(Y)
w2(Y)''')

    def _submit(self):
        schedule_file = StringIO(self.input_area.toPlainText())
        try:
            graph = generate_serializability_graph(schedule_file)
        except ParseError as error:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Parse error',
                              str(error)).exec_()
            return
        finally:
            schedule_file.close()

        is_conflict_serializable = (
            networkx.algorithms.simple_cycles(
                networkx.from_pydot(graph)) == [])
        self.conflict_serializable_label.setText(
            'This schedule is{0} conflict serializable.'.format(
                '' if is_conflict_serializable else ' not'))

        self.output_area.load(QtCore.QByteArray(
            graph.create(prog='dot',  # default
                         format='svg')))


def main(argv):
    app = QtGui.QApplication(argv)

    win = MainWindow()
    win.showMaximized()
    win.raise_()

    app.exec_()
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
