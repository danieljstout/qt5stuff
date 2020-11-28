import sys
from time import sleep
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import speedtest

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time 
import traceback, sys

class WorkerSignals(QObject): 
    ''' Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress
    progress_txt
        `str` indicating what step the worker is working on

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    progress_txt = pyqtSignal(str)

class Worker(QRunnable): 
    ''' Worker thread
    python

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_percentage_callback'] = self.signals.progress
        self.kwargs['progress_text_callback'] = self.signals.progress_txt

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class myMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        # super(myMainWindow, self).__init__(parent, *args, **kwargs)
        super().__init__()
        self.threadpool = QThreadPool()
        self.window()

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
        self.SpeedTestButton.clicked.connect(self.start_speed_test)

    def results_lbl_el(self, widget, x, y):
        self.resultsLabel = QLabel(widget)
        self.resultsLabel.setText('')
        self.resultsLabel.move(x, y)


    ### Event handlers AKA slots ###

    def quit_button_click(self):
        exit()

    def start_speed_test(self):
        self.results_lbl_set_text("Testing Internet speed of things")
        self.speed_test_worker = Worker(self.speed_test)
        self.speed_test_worker.signals.progress_txt.connect(self.results_lbl_set_text)
        self.speed_test_worker.signals.result.connect(self.results_lbl_set_text)
        self.threadpool.start(self.speed_test_worker)

    def speed_test(self, progress_text_callback, progress_percentage_callback):
        progress_text_callback.emit("Connecting...")
        # attempt speed test
        servers = []
        threads = 1

        s = speedtest.Speedtest()
        progress_text_callback.emit("Finding servers...")
        s.get_servers(servers)
        progress_text_callback.emit("Determining best server...")
        s.get_best_server()
        progress_text_callback.emit("Testing download speed...")
        s.download(threads=threads)
        progress_text_callback.emit("Testing upload speed...")
        s.upload(threads=threads)
        # s.results.share()
        results_dict = s.results.dict()
        download_simple = f"{results_dict['download'] / 1_000_000}MBps"
        # self.download_result["text"] = download_simple
        return f"Your download speed is {round((results_dict['download'] / 1_000_000), 2)} MBps"

    def results_lbl_set_text(self, str):
        self.resultsLabel.setText(str)
        self.resultsLabel.adjustSize()

    def update_ui(self):
        print("Now that we're done doing the stuff, this other thing happened on the UI!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    the_best_worker = myMainWindow()
    sys.exit(app.exec_())
