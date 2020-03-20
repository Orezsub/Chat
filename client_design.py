# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 340)
        MainWindow.setMinimumSize(QtCore.QSize(650, 340))
        MainWindow.setMaximumSize(QtCore.QSize(650, 340))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TEdit_Chat_Text = QtWidgets.QTextEdit(self.centralwidget)
        self.TEdit_Chat_Text.setEnabled(True)
        self.TEdit_Chat_Text.setGeometry(QtCore.QRect(130, 30, 521, 281))
        self.TEdit_Chat_Text.setReadOnly(True)
        self.TEdit_Chat_Text.setObjectName("TEdit_Chat_Text")
        self.TEdit_Input_Message = QtWidgets.QTextEdit(self.centralwidget)
        self.TEdit_Input_Message.setGeometry(QtCore.QRect(130, 310, 441, 30))
        self.TEdit_Input_Message.setMaximumSize(QtCore.QSize(661, 16777215))
        self.TEdit_Input_Message.setObjectName("TEdit_Input_Message")
        self.Btn_Send_Message = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_Send_Message.setEnabled(False)
        self.Btn_Send_Message.setGeometry(QtCore.QRect(570, 310, 81, 31))
        self.Btn_Send_Message.setObjectName("Btn_Send_Message")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 651, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Edit_Name = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.Edit_Name.setObjectName("Edit_Name")
        self.horizontalLayout.addWidget(self.Edit_Name)
        self.Edit_IP = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.Edit_IP.setWhatsThis("")
        self.Edit_IP.setInputMask("")
        self.Edit_IP.setText("")
        self.Edit_IP.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.Edit_IP.setObjectName("Edit_IP")
        self.horizontalLayout.addWidget(self.Edit_IP)
        self.Edit_Port = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.Edit_Port.setObjectName("Edit_Port")
        self.horizontalLayout.addWidget(self.Edit_Port)
        self.Btn_Find_Server = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Btn_Find_Server.setObjectName("Btn_Find_Server")
        self.horizontalLayout.addWidget(self.Btn_Find_Server)
        self.Btn_History_Request = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Btn_History_Request.setEnabled(False)
        self.Btn_History_Request.setObjectName("Btn_History_Request")
        self.horizontalLayout.addWidget(self.Btn_History_Request)
        self.Btn_Log_In = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Btn_Log_In.setObjectName("Btn_Log_In")
        self.horizontalLayout.addWidget(self.Btn_Log_In)
        self.Btn_Log_Out = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Btn_Log_Out.setEnabled(False)
        self.Btn_Log_Out.setObjectName("Btn_Log_Out")
        self.horizontalLayout.addWidget(self.Btn_Log_Out)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 50, 131, 291))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 129, 289))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 131, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.ComboBox_Of_Clients = QtWidgets.QComboBox(self.centralwidget)
        self.ComboBox_Of_Clients.setGeometry(QtCore.QRect(0, 30, 131, 22))
        self.ComboBox_Of_Clients.setObjectName("ComboBox_Of_Clients")
        self.ComboBox_Of_Clients.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TEdit_Input_Message.setPlaceholderText(_translate("MainWindow", "Input message"))
        self.Btn_Send_Message.setText(_translate("MainWindow", "Send"))
        self.Edit_Name.setPlaceholderText(_translate("MainWindow", "Input your name"))
        self.Edit_IP.setPlaceholderText(_translate("MainWindow", "server ip"))
        self.Edit_Port.setPlaceholderText(_translate("MainWindow", "port"))
        self.Btn_Find_Server.setText(_translate("MainWindow", "Find"))
        self.Btn_History_Request.setText(_translate("MainWindow", "History"))
        self.Btn_Log_In.setText(_translate("MainWindow", "Log In"))
        self.Btn_Log_Out.setText(_translate("MainWindow", "Log Out"))
        self.ComboBox_Of_Clients.setItemText(0, _translate("MainWindow", "Global"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
