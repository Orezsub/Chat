# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 300)
        MainWindow.setMinimumSize(QtCore.QSize(850, 300))
        MainWindow.setMaximumSize(QtCore.QSize(850, 300))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(850, 300))
        self.centralwidget.setMaximumSize(QtCore.QSize(850, 300))
        self.centralwidget.setObjectName("centralwidget")
        self.TEdit_for_server_info = QtWidgets.QTextEdit(self.centralwidget)
        self.TEdit_for_server_info.setGeometry(QtCore.QRect(0, 0, 850, 300))
        self.TEdit_for_server_info.setMinimumSize(QtCore.QSize(850, 300))
        self.TEdit_for_server_info.setMaximumSize(QtCore.QSize(850, 300))
        self.TEdit_for_server_info.setReadOnly(True)
        self.TEdit_for_server_info.setObjectName("TEdit_for_server_info")
        # MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
