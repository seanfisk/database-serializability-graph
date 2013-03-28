#!/usr/bin/env python
""":mod:`serial_graph.gui` -- Graphical interface
"""

import sys
from cStringIO import StringIO

from PySide import QtCore, QtGui, QtSvg

from serial_graph.graph import generate_serializability_graph, ParseError


class SvgWidget(QtSvg.QSvgWidget):
    def sizeHint(self):
        return super(SvgWidget, self).sizeHint() * 3


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
        self.central_layout.addLayout(self.form_layout, 1)

        self.output_area = SvgWidget()
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                        QtGui.QSizePolicy.MinimumExpanding)
        self.output_area.setSizePolicy(size_policy)
        self.central_layout.addWidget(
            self.output_area, 1, QtCore.Qt.AlignCenter)

        self.setCentralWidget(self.central_widget)

        self._load_default_data()
        self._submit_button_clicked()

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

    def _submit_button_clicked(self):
        schedule_file = StringIO(self.input_area.toPlainText())
        try:
            graph = generate_serializability_graph(schedule_file)
        except ParseError as error:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Parse error',
                              str(error)).exec_()
            return
        finally:
            schedule_file.close()

        output_svg_file = StringIO()
        graph.draw(output_svg_file, format='svg')
        self.output_area.load(QtCore.QByteArray(output_svg_file.getvalue()))
        output_svg_file.close()


def main(argv):
    app = QtGui.QApplication(argv)

    win = MainWindow()
    win.showMaximized()
    win.raise_()

    app.exec_()
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
