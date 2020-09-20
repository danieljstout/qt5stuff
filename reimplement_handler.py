#!/usr/bin/python

"""
ZetCode PyQt5 tutorial

In this example, we reimplement an
event handler.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    def keyPressEvent(self, e):
        modifiers = QApplication.keyboardModifiers()
        if e.key() == Qt.Key_Escape:
            self.close()

        if modifiers == Qt.ControlModifier:
            print("I have control")
        if e.key() == Qt.Key_N:
            print("Yep, I'm pressing the N key!")




def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()