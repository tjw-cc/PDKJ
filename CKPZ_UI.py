# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CKPZ.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from  PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QTimer
import serial
import serial.tools.list_ports
# from CANWindows_UI import CAN_OpenFlag
#import CANWindows_UI

Port = QSerialPort()
Serial_Port = serial.Serial()
Timer_SendMessage = QTimer()
Timer_ReadMessage = QTimer()
Timer_500ms = QTimer()
Timer_SaveEXCEL = QTimer()

SeralPor_OpenFlag = 0
SerialPort_Information = ''

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(474, 451)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(100, 10, 78, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(11, 11, 60, 16))
        self.label.setObjectName("label")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 60, 71, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 75, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(310, 260, 99, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 270, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 110, 54, 21))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 60, 16))
        self.label_4.setObjectName("label_4")
        self.comboBox_4 = QtWidgets.QComboBox(Form)
        self.comboBox_4.setGeometry(QtCore.QRect(100, 160, 38, 21))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_5 = QtWidgets.QComboBox(Form)
        self.comboBox_5.setGeometry(QtCore.QRect(100, 210, 87, 21))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 210, 72, 15))
        self.label_5.setObjectName("label_5")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 320, 99, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(210, 50, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(280, 20, 91, 20))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.Show_ComList)
        self.pushButton_2.clicked.connect(self.Open_Com)
        self.pushButton_3.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def Open_Com(self):
        #self.textBrowser.append("打开成功!!!")
        global SeralPor_OpenFlag
        global SerialPort_Information
        # if CAN_OpenFlag == 1:
        #     return
        if self.pushButton_2.text() == "打开串口" :
            Serial_Port.baudrate = int(self.comboBox.currentText())
            Serial_Port.port = str(self.comboBox_2.currentText())
            Serial_Port.bytesize = int(self.comboBox_3.currentText())
            Serial_Port.stopbits = int(self.comboBox_4.currentText())
            self.str = str(self.comboBox_5.currentText())
            Serial_Port.parity = self.str[0:1]

            try:
                Serial_Port.open()
            except:
                self.textBrowser.append("打开失败,请检测COM口是否有效或是否已经被别的程序打开！！")
                return None

            if Serial_Port.isOpen():
                self.textBrowser.append("打开成功!!!")
                self.pushButton_2.setText(QtCore.QCoreApplication.translate("Form", "关闭串口"))
                self.comboBox.setEnabled(False)
                self.comboBox_2.setEnabled(False)
                self.comboBox_3.setEnabled(False)
                self.comboBox_4.setEnabled(False)
                self.comboBox_5.setEnabled(False)
                Timer_ReadMessage.start(500)
                SeralPor_OpenFlag = 1
                SerialPort_Information = '串口' + str(Serial_Port.port) + '  波特率：' + str(Serial_Port.baudrate)
        elif self.pushButton_2.text() == "关闭串口" :
            self.Close_Com()

    def Message_Deal(self):
        Send_Delay2 = 1

    def Close_Com(self):
        global SeralPor_OpenFlag
        self.textBrowser.clear()
        Serial_Port.close()
        self.textBrowser.append("串口关闭!!!")
        self.pushButton_2.setText(QtCore.QCoreApplication.translate("Form", "打开串口"))
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.comboBox_3.setEnabled(True)
        self.comboBox_4.setEnabled(True)
        self.comboBox_5.setEnabled(True)
        Timer_ReadMessage.stop()
        Timer_SendMessage.stop()
        SeralPor_OpenFlag = 0



    def Message_Read(self):
        Send_Delay2 = 1

    def Show_ComList(self):
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.textBrowser.clear()
        for Port_Com in port_list:
            self.Com_Dict["%s" % Port_Com[0]] = "%s" % Port_Com[1]
            self.textBrowser.append("串口号:")
            self.textBrowser.append(Port_Com[0])  # 返回串口号，如COM1
            # self.textBrowser.append("设备硬件:")
            # self.textBrowser.append(port[0])  # 返回设备硬件描述 如USB-SERIAL CH340
            # self.textBrowser.append("设备编号:")
            # self.textBrowser.append(str(port[0]))  # 返回设备编号 如29987
            # self.textBrowser.append("支持波特率:")
            # Baud_List =  com.standardBaudRates()
            # for Baud in Baud_List:
            #     self.textBrowser.append(str(Baud))  # 返回设备的支持波特率列表 如[110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 56000, 57600, 115200, 128000, 256000]

        if len(self.Com_Dict) == 0:
            self.textBrowser.append("无串口")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "串口配置"))
        Form.setWindowIcon(QIcon("..\Picture\CKPZWindowsTitle.jpg"))
        Form.setToolTip(_translate("Form", "<html><head/><body><p>&amp;串口配置</p></body></html>"))
        self.comboBox.setItemText(0, _translate("Form", "9600"))
        self.comboBox.setItemText(1, _translate("Form", "19200"))
        self.comboBox.setItemText(2, _translate("Form", "115200"))
        self.label.setText(_translate("Form", "波特率："))
        self.comboBox_2.setItemText(0, _translate("Form", "COM1"))
        self.comboBox_2.setItemText(1, _translate("Form", "COM2"))
        self.comboBox_2.setItemText(2, _translate("Form", "COM3"))
        self.comboBox_2.setItemText(3, _translate("Form", "COM4"))
        self.comboBox_2.setItemText(4, _translate("Form", "COM5"))
        self.comboBox_2.setItemText(5, _translate("Form", "COM6"))
        self.comboBox_2.setItemText(6, _translate("Form", "COM7"))
        self.comboBox_2.setItemText(7, _translate("Form", "COM8"))
        self.comboBox_2.setItemText(8, _translate("Form", "COM9"))
        self.comboBox_2.setItemText(9, _translate("Form", "COM10"))
        self.comboBox_2.setItemText(10, _translate("Form", "COM11"))
        self.comboBox_2.setItemText(11, _translate("Form", "COM12"))
        self.comboBox_2.setItemText(12, _translate("Form", "COM13"))
        self.comboBox_2.setItemText(13, _translate("Form", "COM14"))
        self.comboBox_2.setItemText(14, _translate("Form", "COM15"))
        self.label_2.setText(_translate("Form", "串口选择："))
        self.pushButton.setText(_translate("Form", "自动选择串口"))
        self.pushButton_2.setText(_translate("Form", "打开串口"))
        self.comboBox_3.setItemText(0, _translate("Form", "8"))
        self.comboBox_3.setItemText(1, _translate("Form", "7"))
        self.comboBox_3.setItemText(2, _translate("Form", "6"))
        self.label_3.setText(_translate("Form", "数据位："))
        self.label_4.setText(_translate("Form", "停止位："))
        self.comboBox_4.setItemText(0, _translate("Form", "1"))
        self.comboBox_4.setItemText(1, _translate("Form", "1.5"))
        self.comboBox_4.setItemText(2, _translate("Form", "2"))
        self.comboBox_5.setItemText(0, _translate("Form", 'None'))
        self.comboBox_5.setItemText(1, _translate("Form", 'Even'))
        self.comboBox_5.setItemText(2, _translate("Form", 'Odd'))
        self.comboBox_5.setItemText(3, _translate("Form", 'Mark'))
        self.comboBox_5.setItemText(4, _translate("Form", 'Space'))
        self.label_5.setText(_translate("Form", "检验位"))
        self.pushButton_3.setText(_translate("Form", "关闭窗口"))
        self.label_6.setText(_translate("Form", "可用串口列表"))

