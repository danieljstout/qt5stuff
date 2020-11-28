import sys
from time import sleep
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class WorkerSignals(QObject):
    new_data = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def monitorDataThread(self, *args, **kwargs):
        print("Doing stuff....")
        sleep(20)
        print("I totally just did stuff")
        self.signals.new_data.emit()


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
        self.monitor_data_button(self, 210, 210)
        self.show()

    def quit_button(self, widget, x, y):
        self.quitButton = QPushButton(widget)
        self.quitButton.setText("quit")
        self.quitButton.move(x, y)
        self.quitButton.setStyleSheet("background-color: red")
        self.quitButton.clicked.connect(self.quit_button_click)

    def monitor_data_button(self, widget, x, y):
        self.MonitorDataButton = QPushButton(widget)
        self.MonitorDataButton.setText("Begin monitoring")
        self.MonitorDataButton.move(x, y)
        self.MonitorDataButton.setStyleSheet("background-color: green")
        self.MonitorDataButton.clicked.connect(self.monitor_data)
        


    ### Event handlers AKA slots ###

    def quit_button_click(self):
        exit()

    def monitor_data(self):
        print("Kicking off the worker")
        self.monitor_data_worker = Worker()
        self.monitor_data_worker.signals.new_data.connect(self.update_ui)
        self.threadpool.start(self.monitor_data_worker.monitorDataThread)

    def update_ui(self):
        print("Now that we're done doing the stuff, this other thing happened on the UI!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    the_best_worker = myMainWindow()
    the_best_worker.window()
    sys.exit(app.exec_())
