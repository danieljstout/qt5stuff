import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class helloQT:
    def __init__(self):
        self.click_count = 0

    def window(self):
        app = QApplication(sys.argv)
        widget = QWidget()

        clickMeButton = QPushButton(widget)
        clickMeButton.setText("This is a button")
        clickMeButton.move(150, 170)
        clickMeButton.clicked.connect(self.button_clicked)

        self.resetButton = QPushButton(widget)
        self.resetButton.setText("reset")
        self.resetButton.move(150, 210)
        self.resetButton.clicked.connect(self.reset_button_click)
        self.resetButton.hide()

        self.quitButton = QPushButton(widget)
        self.quitButton.setText("quit")
        self.quitButton.move(330, 380)
        self.quitButton.clicked.connect(self.quit_button_click)

        self.buttonlabel = QLabel(widget)
        self.buttonlabel.setText('')
        self.buttonlabel.move(150, 195)

        self.textLabel = QLabel(widget)
        self.textLabel.setText("Hello World!")
        self.textLabel.move(150, 150)

        widget.setGeometry(50, 50, 420, 420)
        widget.setWindowTitle("PyQt5 GTFO")
        widget.show()
        sys.exit(app.exec_())

    def button_clicked(self):
        if self.resetButton.isHidden():
            self.resetButton.show()
        self.click_count += 1
        self.buttonlabel.setText(f"We was clicked dawg {self.click_count} times")
        self.buttonlabel.adjustSize()

    def reset_button_click(self):
        self.click_count = 0
        self.buttonlabel.setText('')
        self.resetButton.hide()


    def quit_button_click(self):
        exit()


if __name__ == '__main__':
    app = helloQT()
    app.window()
