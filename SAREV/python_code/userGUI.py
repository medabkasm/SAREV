# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userGUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.ps1 = QtWidgets.QPushButton(Dialog)
        self.ps1.setGeometry(QtCore.QRect(160, 80, 89, 25))
        self.ps1.setObjectName("ps1")
        self.ps2 = QtWidgets.QPushButton(Dialog)
        self.ps2.setGeometry(QtCore.QRect(160, 120, 89, 25))
        self.ps2.setObjectName("ps2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 190, 67, 17))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ps1.setText(_translate("Dialog", "PushButton"))
        self.ps2.setText(_translate("Dialog", "PushButton"))
        self.label.setText(_translate("Dialog", "TextLabel"))

