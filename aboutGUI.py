# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutSensei.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.resize(310, 238)
        AboutWindow.setAutoFillBackground(False)
        self.label = QtWidgets.QLabel(AboutWindow)
        self.label.setGeometry(QtCore.QRect(80, 30, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Futura")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AboutWindow)
        self.label_2.setGeometry(QtCore.QRect(80, 50, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AboutWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 60, 80))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("meditate-small.png"))
        self.label_3.setObjectName("label_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(AboutWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 170, 160, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.updatesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.updatesButton.setAutoDefault(False)
        self.updatesButton.setObjectName("updatesButton")
        self.verticalLayout.addWidget(self.updatesButton)
        self.horizontalLayoutWidget = QtWidgets.QWidget(AboutWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 292, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.supportButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.supportButton.setFont(font)
        self.supportButton.setAutoDefault(False)
        self.supportButton.setObjectName("supportButton")
        self.horizontalLayout.addWidget(self.supportButton)
        self.githubButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.githubButton.setAutoDefault(False)
        self.githubButton.setObjectName("githubButton")
        self.horizontalLayout.addWidget(self.githubButton)

        self.retranslateUi(AboutWindow)
        QtCore.QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        _translate = QtCore.QCoreApplication.translate
        AboutWindow.setWindowTitle(_translate("AboutWindow", "About Sensei"))
        self.label.setText(_translate("AboutWindow", "Sensei"))
        self.label_2.setText(
            _translate("AboutWindow", "Copyright 2016-2017 Justin Shenk\n"
                       "Version 0.1"))
        self.updatesButton.setText(
            _translate("AboutWindow", "Check for updates"))
        self.supportButton.setText(_translate("AboutWindow", "Support Sensei"))
        self.githubButton.setText(
            _translate("AboutWindow", "Visit GitHub Repo"))
