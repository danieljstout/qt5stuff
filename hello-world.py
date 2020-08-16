import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import speedtest


class helloQT:
    def __init__(self):
        self.click_count = 0

    def window(self):
        app = QApplication(sys.argv)
        widget = QWidget()

        # buttons
        self.click_me_btn_el(widget, 180, 80)
        self.reset_btn_el(widget, 180, 120)
        self.quit_btn_el(widget, 330, 380)

        # labels
        self.clicked_lbl_el(widget, 180, 105)
        self.hello_lbl_el(widget, 180, 15)

        # speed test stuff
        self.speed_test_btn_el(widget, 25, 195)
        self.results_lbl_el(widget, 25, 220)

        widget.setGeometry(50, 50, 420, 420)
        widget.setWindowTitle("PyQt5 GTFO")
        widget.show()
        sys.exit(app.exec_())

    def click_me_btn_el(self, widget, x, y):
        self.clickMeButton = QPushButton(widget)
        self.clickMeButton.setText("click this button")
        self.clickMeButton.move(x, y)
        self.clickMeButton.clicked.connect(self.button_clicked)

    def speed_test_btn_el(self, widget, x, y):
        self.speedTestButton = QPushButton(widget)
        self.speedTestButton.setText("Test Your Internet Speed")
        self.speedTestButton.move(x, y)
        self.speedTestButton.clicked.connect(self.speed_test)


    def reset_btn_el(self, widget, x, y):
        self.resetButton = QPushButton(widget)
        self.resetButton.setText("reset")
        self.resetButton.move(x, y)
        self.resetButton.clicked.connect(self.reset_button_click)
        self.resetButton.hide()

    def quit_btn_el(self, widget, x, y):
        self.quitButton = QPushButton(widget)
        self.quitButton.setText("quit")
        self.quitButton.move(x, y)
        self.quitButton.setStyleSheet("background-color: red")
        self.quitButton.clicked.connect(self.quit_button_click)

    def clicked_lbl_el(self, widget, x, y):
        self.buttonlabel = QLabel(widget)
        self.buttonlabel.setText('')
        self.buttonlabel.move(x, y)

    def hello_lbl_el(self, widget, x, y):
        self.textLabel = QLabel(widget)
        self.textLabel.setText("Hello World!")
        self.textLabel.move(x, y)

    def results_lbl_el(self, widget, x, y):
        self.resultsLabel = QLabel(widget)
        self.resultsLabel.setText('')
        self.resultsLabel.move(x, y)

    def button_clicked(self):
        if self.resetButton.isHidden():
            self.resetButton.show()
        self.click_count += 1
        self.buttonlabel.setText(f"We was clicked dawg {self.click_count} times")
        self.buttonlabel.adjustSize()

    def reset_button_click(self):
        self.click_count = 0
        self.buttonlabel.setText("We wasn't clicked no more")
        self.resetButton.hide()

    def quit_button_click(self):
        exit()

    def results_lbl_set_text(self, str):
        self.resultsLabel.setText(str)
        self.resultsLabel.adjustSize()

    def speed_test(self):
        self.results_lbl_set_text("Connecting...")
        # attempt speed test
        servers = []
        threads = 1

        s = speedtest.Speedtest()
        self.results_lbl_set_text("Finding servers...")
        s.get_servers(servers)
        self.results_lbl_set_text("Determining best server...")
        s.get_best_server()
        self.results_lbl_set_text("Testing download speed...")
        s.download(threads=threads)
        self.results_lbl_set_text("Testing upload speed...")
        s.upload(threads=threads)
        # s.results.share()
        results_dict = s.results.dict()
        download_simple = f"{results_dict['download'] / 1_000_000}MBps"
        # self.download_result["text"] = download_simple
        self.results_lbl_set_text(f"Your download speed is {round((results_dict['download'] / 1_000_000), 2)} MBps")

if __name__ == '__main__':
    app = helloQT()
    app.window()
