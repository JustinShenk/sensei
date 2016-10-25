#!/usr/bin/env python
import cv2
import numpy as np
import os
from PyQt4 import QtCore, QtGui


class Capture():

    def __init__(self):
        self.capturing = False
        self.cascPath = 'haarcascade_frontalface_alt.xml'
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        cv2.namedWindow('Sensei')
        cv2.setMouseCallback('Sensei', self.mouse)
        self.cam = cv2.VideoCapture(0)
        self.screenwidth = 320
        self.screenheight = 480
        self.cam.set(3, self.screenwidth)
        self.cam.set(4, self.screenheight)
        self.currPosX = None
        self.currPosY = None
        self.click_point_x = None
        self.click_point_y = None
        self.calibrated_width = []
        self.width = 0
        self.emoji = cv2.imread('emoticon.png')
        # self.emoji = cv2.cvtColor(self.emoji, cv2.COLOR_BGR2GRAY)
        self.scale = 0.5
        self.color = (0, 0, 255)
        self.tickCount = 0
        self.seconds = 5
        self.level = 1

    def startCapture(self):
        print "pressed start"
        self.capturing = True
        if (self.capturing):
            self.play()

    def endCapture(self):
        print "pressed End"
        self.capturing = False

    def quitCapture(self):
        print "pressed Quit"
        cap = self.cam
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()

    def mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE and not self.currPosX:
            self.currPosX, self.currPosY = x, y
            print x, y
        if event == cv2.EVENT_LBUTTONUP and not self.click_point_x:
            # click_point_x, click_point_y = x, y
            self.calibrated_width.append(self.width)
            print "width", self.calibrated_width[0]

    def reset_mouse(self):
        self.click_point_x = -1
        self.click_point_y = -1

    def notify(title, subtitle, message):
        t = '-title {!r}'.format(title)
        s = '-subtitle {!r}'.format(subtitle)
        m = '-message {!r}'.format(message)
        os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

    def play(self):
        while (self.level == 1):
            success, frame = self.cam.read()
            self.tickCount += 1
            # if frameId % multiplier == 0:
            #     pass
            # else:
            #     continue
            # # Capture frame-by-frame

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mask = np.zeros_like(gray)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=2,
                minSize=(100, 100),
                #         flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                flags=0
            )

            for (x, y, w, h) in faces:
                self.width = w
                # cv2.rectangle(mask, (4 * screenwidth / 5, screenheight / 2), (4 *
                # screenwidth / 5, screenheight / 2), color=244, -1)

                mask[y:y + h, x:x + w] = 190
                mask = cv2.blur(mask, (24, 24))

                # if y + self.emoji.shape[1] < self.screenheight and x +
                # self.emoji.shape[0] < self.screenwidth:

                #     mask[y:y + self.emoji.shape[0],
                #          x:x + self.emoji.shape[1]] = self.emoji

                cv2.putText(mask, "Select proper distance",
                            (1 * self.screenwidth / 5 + 10, 2 * self.screenheight / 3 + 20), cv2.FONT_HERSHEY_SIMPLEX, self.scale, color=200)
                cv2.putText(mask, np.array_str(w), (x, y + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, self.scale, self.color)
            if len(faces) < 1:
                cv2.putText(mask, "Sit back",
                            (1 * self.screenwidth / 5 + 10, 2 * self.screenheight / 3 + 20), cv2.FONT_HERSHEY_SIMPLEX, self.scale, color=200)
            # Display the resulting frame
            cv2.imshow('Sensei', mask)

            if len(self.calibrated_width) > 0:
                self.level += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        while (self.level == 2):
            self.tickCount += 1
            cv2.destroyWindow('Sensei')
            # Only sample frame every x ticks
            if self.tickCount % 500 is not 0:
                pass
            else:
                print "next"
                self.cam = cv2.VideoCapture(0)
                success, frame = self.cam.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.tickCount += 1
                faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(100, 100),
                                                          # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                                                          flags=0
                                                          )

                for (x, y, w, h) in faces:
                    print "w", w, "calibrated_width", self.calibrated_width[0]
                    if w > self.calibrated_width[0]:
                        # Calling the function
                        print w, self.calibrated_width[0]
                        self.notify(title='Sensei',
                                    subtitle='Whack!',
                                    message='Sit up strait, grasshopper')
                    else:
                        # cv2.rectangle(gray, (x, y), (x + w, y + h),
                        #               (0, 255, 0), 2)
                        pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


class Window(QtGui.QWidget):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self.capture = Capture()
        self.start_button = QtGui.QPushButton('Start', self)
        self.start_button.clicked.connect(self.capture.startCapture)

        self.end_button = QtGui.QPushButton('End', self)
        self.end_button.clicked.connect(self.capture.endCapture)

        self.quit_button = QtGui.QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.capture.quitCapture)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.quit_button)

        self.setLayout(vbox)
        self.setGeometry(100, 100, 200, 200)
        self.show()
        self.raise_()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

# pdb.set_trace()
