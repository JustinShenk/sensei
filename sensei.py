# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import sys
import pickle
import argparse
import datetime
# import subprocess

from cv2 import (VideoCapture, waitKey, CascadeClassifier,
                 cvtColor, COLOR_BGR2GRAY)

from PyQt5.QtWidgets import (QPushButton, QApplication, QProgressBar,
                             QLabel, QGraphicsOpacityEffect, QInputDialog, QWidget, qApp, QAction, QMenuBar, QMenu, QSystemTrayIcon, QMainWindow)
from PyQt5.QtCore import (QCoreApplication, QObject,
                          QThread, QTimer, QRect, QEasingCurve, QPropertyAnimation)
from PyQt5.QtGui import QIcon, QCheckBox

# CASCPATH = "/usr/local/opt/opencv3/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
# FACECASCADE = cv2.CascadeClassifier(CASCPATH)

# Delay between checking posture in miliseconds.
MONITOR_DELAY = 2000

# Notify when user is 1.2 times closer than the calibration distance.
SENSITIVITY = 1.2
CALIBRATION_SAMPLE_RATE = 100

USER_ID = None
SESSION_ID = None
TERMINAL_NOTIFIER_INSTALLED = None


def getPath(path):
    """ Get absolute path to resource, works for dev and PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, path)


CASCPATH = getPath('face.xml')
FACECASCADE = CascadeClassifier(CASCPATH)

APP_ICON_PATH = getPath('posture.png')


def trace(frame, event, arg):
    print(("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno)))
    return trace


def getFaces(frame):
    gray = cvtColor(frame, COLOR_BGR2GRAY)
    faces = FACECASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(100, 100),
        #         flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        flags=0
    )
    if len(faces):
        print("Face found: ", faces[0])
    return faces


class Sensei(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.history = {}
        self.history[USER_ID] = {}
        self.history[USER_ID][SESSION_ID] = {}
        # Create the worker Thread
        # TODO: See if any advantage to using thread or if timer alone works.
        # TODO: Compare to workerThread example at
        # https://stackoverflow.com/questions/31945125/pyqt5-qthread-passing-variables-to-main
        self.capture = Capture(self)

        self.timer = QTimer(self, timeout=self.calibrate)
        self.mode = 0  # 0: Initial, 1: Calibrate, 2: Monitor
        self.checkDependencies()

    def checkDependencies(self):
        global TERMINAL_NOTIFIER_INSTALLED

        if 'darwin' in sys.platform and not TERMINAL_NOTIFIER_INSTALLED:
            # FIXME: Add check for Brew installation and installation of
            # terminal-notifier.
            self.instructions.setText(
                'Installing terminal-notifier dependency')
            print('Installing terminal-notifier is required')
            # FIXME: This line hangs.
            # subprocess.call(
            #     ['brew', 'install', 'terminal-notifier'], stdout=subprocess.PIPE)
            # TERMINAL_NOTIFIER_INSTALLED = True
            self.instructions.setText('Sit upright and click \'Calibrate\'')

    def closeEvent(self, event):
        """ Override QWidget close event to save history on exit. """
        # TODO: Replace with CSV method.
        # if os.path.exists('posture.dat'):
        #     with open('posture.dat','rb') as saved_history:
        #         history =pickle.load(saved_history)
        if self.history:
            if hasattr(sys, "_MEIPASS"):  # PyInstaller deployed
                here = os.path.join(sys._MEIPASS)
            else:
                here = os.path.dirname(os.path.realpath(__file__))
            directory = os.path.join(here, 'data', str(USER_ID))
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(os.path.join(directory, str(SESSION_ID) + '.dat'), 'wb') as f:
                pickle.dump(self.history, f)
        qApp.quit()

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def initUI(self):

        menu = QMenu()
        iconPath = getPath('exit.png')
        self.trayIcon = QSystemTrayIcon(self)
        supported = self.trayIcon.supportsMessages()
        self.trayIcon.setIcon(QIcon(iconPath))
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.showMessage('a', 'b')
        self.trayIcon.show()

        self.postureIcon = QSystemTrayIcon(self)
        self.postureIcon.setIcon(QIcon(getPath('posture.png')))
        self.postureIcon.setContextMenu(menu)
        self.postureIcon.show()

        exitAction = QAction(QIcon(iconPath), "&Exit", self, shortcut="Ctrl+Q",
                             triggered=self.closeEvent)
        exitAction.setStatusTip('Exit Program')
        openAction = QAction(QIcon(iconPath), "&Open",
                             self, triggered=self.showApp)
        openAction.setStatusTip('Open Sensei')

        menu.addAction(openAction)
        menu.addSeparator()
        menu.addAction(exitAction)

        # TODO: Add settings panel.
        # changeSettings = QAction(QIcon('exit.png'), "&Settings", self, shortcut="Cmd+,", triggered=self.changeSettings)
        # changeSettings.setStatusTip('Change Settings')
        # menu.addAction(changeSettings)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbarValue = 0
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Posture Monitor')

        self.startButton = QPushButton('Calibrate', self)
        self.startButton.move(30, 60)
        self.startButton.clicked.connect(self.calibrate)
        self.stopButton = QPushButton('Stop', self)
        self.stopButton.move(30, 60)
        self.stopButton.clicked.connect(self.endCalibration)
        self.stopButton.hide()
        self.settingsButton = QPushButton('Settings', self)
        self.settingsButton.move(140, 60)
        self.settingsButton.clicked.connect(self.settings)

        self.doneButton = QPushButton('Done', self)
        self.doneButton.move(30, 60)
        self.doneButton.hide()
        self.doneButton.clicked.connect(self.minimize)
        # TODO: Create QWidget panel for Settings with MONITOR_DELAY
        # and SENSITIVITY options.
        # layout = QFormLayout()
        # self.le = QLineEdit()

        self.instructions = QLabel(self)
        self.instructions.move(40, 20)
        self.instructions.setText('Sit upright and click \'Calibrate\'')
        self.instructions.setGeometry(40, 20, 230, 25)

        if not supported:
            self.instructions.setText(
                'Error: Notification is not available on your system.')
        self.show()

    # # TODO: Add settings panel.
    # def changeSettings(self):
    #     pass

    def minimize(self):
        self.reset()
        self.hide()

    def reset(self):
        pass

    def showApp(self):
        self.show()
        self.raise_()
        self.doneButton.hide()
        self.startButton.show()
        self.pbar.show()
        self.settingsButton.show()
        self.activateWindow()

    def settings(self):
        global MONITOR_DELAY
        seconds, ok = QInputDialog.getInt(
            self, "Delay Settings", "Enter number of seconds to check posture\n(Default = 5)")
        if ok:
            seconds = seconds if seconds >= 1 else 0.5
            MONITOR_DELAY = seconds * 1000

    def endCalibration(self):
        self.mode = 2  # Monitor mode
        self.timer.stop()
        self.stopButton.hide()
        self.startButton.setText('Recalibrate')  # Keep hidden.
        self.instructions.setText('Sit upright and click \'Recalibrate\'')
        self.instructions.hide()
        self.pbar.hide()
        self.settingsButton.hide()

        self.animateClosing()

        # Begin monitoring posture.
        self.timer = QTimer(self, timeout=self.monitor)
        self.timer.start(MONITOR_DELAY)

    def animateClosing(self):
        self.doneButton.show()
        animation = QPropertyAnimation(self.doneButton, b"geometry")
        animation.setDuration(1000)
        animation.setStartValue(QRect(10, 60, 39, 20))
        animation.setEndValue(QRect(120, 60, 39, 20))
        animation.start()
        self.animation = animation

    def monitor(self):
        """ 
        Grab the picture, find the face, and sent notification 
        if needed.
        """
        photo = self.capture.takePhoto()
        faces = getFaces(photo)
        while not len(faces):
            print("No faces detected.")
            time.sleep(2)
            photo = self.capture.takePhoto()
            faces = getFaces(photo)
        # Record history for later analyis.
        # TODO: Make this into cvs-friendly format.
        self.history[USER_ID][SESSION_ID][datetime.datetime.now().strftime(
            '%Y-%m-%d_%H-%M-%S')] = faces
        x, y, w, h = faces[0]
        if w > self.upright * SENSITIVITY:
            self.notify(title='Sensei 🙇👊',  # TODO: Add doctor emoji `👨‍⚕️`
                        subtitle='Whack!',
                        message='Sit up strait 🙏⛩',
                        appIcon='APP_ICON_PATH'
                        )

        # self.trayIcon.toolTip("tool tip")

    def notify(self, title, subtitle, message, sound=None, appIcon=None):
        """ 
        Mac-only and requires `terminal-notifier` to be installed.
        # TODO: Add check that terminal-notifier is installed.
        # TODO: Add Linux and windows compatibility.
        # TODO: Linux example:
        # TODO: sudo apt-get install libnotify-bin
        # TODO: from gi.repository import Notify
        # TODO: Notify.init("App Name")
        # TODO: Notify.Notification.new("Hi").show()
        """
        # FIXME: Test following line on windows / linux.
        # Doesn't work on Mac and might replace `terminal-notifier` dependency
        # self.trayIcon.showMessage('Title', 'Content')
        if 'darwin' in sys.platform and TERMINAL_NOTIFIER_INSTALLED:  # Check if on a Mac.
            t = '-title {!r}'.format(title)
            s = '-subtitle {!r}'.format(subtitle)
            m = '-message {!r}'.format(message)
            snd = '-sound {!r}'.format(sound)
            i = '-appIcon {!r}'.format(appIcon)
            os.system(
                'terminal-notifier {}'.format(' '.join([m, t, s, snd, i])))
        else:
            self.trayIcon.showMessage(
                "Sit up strait 🙇👊", "News", QSystemTrayIcon.Information, 4000)

    def calibrate(self):
        if self.mode == 2:  # Came from 'Recalibrate'
            # Set up for calibrate mode.
            self.mode = 1
            self.stopButton.show()
            self.startButton.hide()
            self.instructions.setText('Press \'stop\' when ready')
            self.timer.stop()
            self.timer = QTimer(self, timeout=self.calibrate)
            self.timer.start(CALIBRATION_SAMPLE_RATE)
        # Interpolate posture information from face.
        photo = self.capture.takePhoto()
        faces = getFaces(photo)
        while not len(faces):
            print("No faces detected.")
            time.sleep(2)
            photo = self.capture.takePhoto()
            faces = getFaces(photo)
        x, y, w, h = faces[0]
        self.upright = w
        if self.mode == 0:  # Initial mode
            self.timer.start(CALIBRATION_SAMPLE_RATE)
            self.startButton.hide()
            self.stopButton.show()
            self.instructions.setText('Press \'stop\' when ready')
            self.mode = 1  # Calibrate mode
        elif self.mode == 1:
            # Update posture monitor bar.
            self.pbar.setValue(self.upright / 4)


class Capture(QThread):

    def __init__(self, window):
        super(Capture, self).__init__(window)
        self.window = window
        self.capturing = False
        self.cam = VideoCapture(0)
        self.cam.set(3, 640)
        self.cam.set(4, 480)

    def takePhoto(self):
        if not self.cam.isOpened():
            self.cam.open(0)
            waitKey(5)
        _, frame = self.cam.read()
        # cv2.imwrite('tst.png', frame)
        waitKey(1)
        # Optional - save image.
        # cv2.imwrite('save.png', frame)
        return frame


def process_cl_args():
    """ Process command line arguments to work with QApplication. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Debug mode",
                        action="store_true")
    # TODO: Add to `Session ID` to settings menu.
    parser.add_argument("-s", "--session", help="Session ID", action="store")
    parser.add_argument("-u", "--user", help="User ID", action="store")

    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args


if __name__ == '__main__':

    parsed_args, unparsed_args = process_cl_args()
    SESSION_ID = parsed_args.session
    USER_ID = parsed_args.user
    # (Debug mode) Set global debug tracing option.
    if parsed_args.debug:
        sys.settrace(trace)

    # Check dependency.
    TERMINAL_NOTIFIER_INSTALLED = True if os.path.exists(
        '/usr/local/bin/terminal-notifier') else False
    # QApplication expects the first argument to be the program name.
    qt_args = sys.argv[:1] + unparsed_args
    app = QApplication(qt_args)
    sensei = Sensei()
    sys.exit(app.exec_())
