import sys
from time import sleep
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import speedtest

class WorkerSignals(QObject):
    new_data = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def speedTestThread(self, *args, **kwargs):
        print("Doing stuff....")
        print("Connecting...")
        # attempt speed test
        servers = []
        threads = 1

        s = speedtest.Speedtest()
        print("Finding servers...")
        s.get_servers(servers)
        print("Determining best server...")
        s.get_best_server()
        print("Testing download speed...")
        s.download(threads=threads)
        print("Testing upload speed...")
        s.upload(threads=threads)
        # s.results.share()
        results_dict = s.results.dict()
        download_simple = f"{results_dict['download'] / 1_000_000}MBps"
        # self.download_result["text"] = download_simple
        print(f"Your download speed is {round((results_dict['download'] / 1_000_000), 2)} MBps")
        self.signals.new_data.emit()
        print("I totally just did stuff")


class myMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        # super(myMainWindow, self).__init__(parent, *args, **kwargs)
        super().__init__()
        self.threadpool = QThreadPool()
        # self.quit_button = 

    def window(self):
        self.setGeometry(0, 0, 420, 420)
        self.setWindowTitle("Workers GTFI")
        self.quit_button(self, 0,0)
        self.speed_test_button(self, 210, 210)
        self.results_lbl_el(self, 210, 270)
        self.show()

    def quit_button(self, widget, x, y):
        self.quitButton = QPushButton(widget)
        self.quitButton.setText("quit")
        self.quitButton.move(x, y)
        self.quitButton.setStyleSheet("background-color: red")
        self.quitButton.clicked.connect(self.quit_button_click)


    def speed_test_button(self, widget, x, y):
        self.SpeedTestButton = QPushButton(widget)
        self.SpeedTestButton.setText("Check Internet Speed")
        self.SpeedTestButton.move(x, y)
        self.SpeedTestButton.setStyleSheet("background-color: blue")
        self.SpeedTestButton.setGeometry(x, y, 200, 42)
        self.SpeedTestButton.clicked.connect(self.speed_test)

    def results_lbl_el(self, widget, x, y):
        self.resultsLabel = QLabel(widget)
        self.resultsLabel.setText('')
        self.resultsLabel.move(x, y)


    ### Event handlers AKA slots ###

    def quit_button_click(self):
        exit()

    def speed_test(self):
        self.results_lbl_set_text("Testing Internet speed of things")
        self.speed_test_worker = Worker()
        self.speed_test_worker.signals.new_data.connect(self.update_ui)
        self.threadpool.start(self.speed_test_worker.speedTestThread)

    def results_lbl_set_text(self, str):
        self.resultsLabel.setText(str)
        self.resultsLabel.adjustSize()

    def update_ui(self):
        print("Now that we're done doing the stuff, this other thing happened on the UI!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    the_best_worker = myMainWindow()
    the_best_worker.window()
    sys.exit(app.exec_())
