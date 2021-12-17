# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crm_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(653, 713)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(140, 580, 331, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.run_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.run_btn.setObjectName("run_btn")
        self.horizontalLayout_3.addWidget(self.run_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.cancel_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_3.addWidget(self.cancel_btn)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 110, 631, 401))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(560, 90, 75, 23))
        self.save_btn.setObjectName("save_btn")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 12, 631, 71))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.source_edit = QtWidgets.QLineEdit(self.widget)
        self.source_edit.setObjectName("source_edit")
        self.horizontalLayout.addWidget(self.source_edit)
        self.source_select = QtWidgets.QPushButton(self.widget)
        self.source_select.setObjectName("source_select")
        self.horizontalLayout.addWidget(self.source_select)
        self.source_open = QtWidgets.QPushButton(self.widget)
        self.source_open.setObjectName("source_open")
        self.horizontalLayout.addWidget(self.source_open)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.out_edit = QtWidgets.QLineEdit(self.widget)
        self.out_edit.setObjectName("out_edit")
        self.horizontalLayout_2.addWidget(self.out_edit)
        self.out_select = QtWidgets.QPushButton(self.widget)
        self.out_select.setObjectName("out_select")
        self.horizontalLayout_2.addWidget(self.out_select)
        self.out_open = QtWidgets.QPushButton(self.widget)
        self.out_open.setObjectName("out_open")
        self.horizontalLayout_2.addWidget(self.out_open)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 653, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.label_3.setBuddy(self.tableWidget)
        self.label.setBuddy(self.source_edit)
        self.label_4.setBuddy(self.out_edit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.source_edit, self.source_select)
        MainWindow.setTabOrder(self.source_select, self.out_edit)
        MainWindow.setTabOrder(self.out_edit, self.out_select)
        MainWindow.setTabOrder(self.out_select, self.run_btn)
        MainWindow.setTabOrder(self.run_btn, self.cancel_btn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.run_btn.setText(_translate("MainWindow", "Run"))
        self.cancel_btn.setText(_translate("MainWindow", "Cancel"))
        self.label_3.setText(_translate("MainWindow", "Source Files:"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Source :"))
        self.source_select.setText(_translate("MainWindow", "Select"))
        self.source_open.setText(_translate("MainWindow", "Open"))
        self.label_4.setText(_translate("MainWindow", "Output :"))
        self.out_select.setText(_translate("MainWindow", "Select"))
        self.out_open.setText(_translate("MainWindow", "Open"))
