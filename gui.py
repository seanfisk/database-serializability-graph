#!/usr/bin/env python

import sys

from PySide import QtGui, QtSvg

def main(argv):
    app = QtGui.QApplication(argv)

    w = QtSvg.QSvgWidget('out.svg')
    w.show()
    w.raise_()

    app.exec_()
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
