import threading
import sys
import time
from PyQt4 import QtCore, QtGui
import psutil
import os


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_layout = QtGui.QVBoxLayout()

        ok_button = QtGui.QPushButton("Run")
        ok_button.clicked.connect(self.OK)
        self.main_layout.addWidget(ok_button)

        cancel_button = QtGui.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        self.main_layout.addWidget(cancel_button)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def myEvenListener(self, stop_event):
        state = True
        while state and not stop_event.isSet():
            for i in range(10, 100):
                time.sleep(i * 0.01)
                print '.' * i

    def OK(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(
            target=self.myEvenListener, args=(self.stop_event,))
        self.c_thread.start()

    def cancel(self):
        self.stop_event.set()
        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(480, 320)
    window.show()
    app.exec_()

main()


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()

me = os.getpid()
kill_proc_tree(me)
