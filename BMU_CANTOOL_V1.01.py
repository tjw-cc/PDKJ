# order:jw time:2022-10-09
# ******************************************
import asyncio
import operator
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from ctypes import c_uint16, c_uint8, c_uint32, c_uint, c_byte
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QApplication

from UISource.DataTurn import DataTurn
from UISource.BMU_BalanceCtrl import BMU_BalanceCtrl
from UISource.BMU_CANCOMDEAL import BMU_CANCOMDEAL

from UISource.PythonMemory import PythonMemory
from UISource.BMU_CANPARASET import BMU_CANPARASET
from UISource.BMU_CANTOOL import Ui_BMU_CANTOOL

Data_RefreshTimer = QTimer()
Data_QueryTimer = QTimer()

CANDeviceNameNumber = 4
CANDeviceIndexNumber = 0
CANDeviceChannelNumber = 0
CANDeviceBoundRate = 0x011C
BMU_Index = 0

Path = '..\Source\DLL\ControlCAN.dll'
CANBuffer = [[0 for x in range(10)] for y in range(50)]  # 50帧的数据缓存

BMUData_Vol = [0 for i in range(24)]
BMUData_Temp = [0 for i in range(24)]
BMUData_Balance = [0 for i in range(24)]
# 日志信息
Browser_Info = ''

# 创建一个容量最大为3的线程池
Pool = ThreadPoolExecutor(3)


# 定义初始化CAN的数据类型
class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_uint16),
                ('AccMask', c_uint16),
                ('Reserved', c_uint16),
                ('Filter', c_uint8),
                ('Timing0', c_uint8),
                ('Timing1', c_uint8),
                ('Mode', c_uint8)]


# 定义CAN信息帧的数据类型
class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint32),
                ('TimeStamp', c_uint32),
                ('TimeFlag', c_uint8),
                ('SendType', c_uint8),
                ('RemoteFlag', c_uint8),
                ('ExternFlag', c_uint8),
                ('DataLen', c_uint8),
                ('Data', c_uint8 * 8),
                ('Reserved', c_uint8 * 3)]


# 定义错误信息类型
class _VCI_ERR_INFO(Structure):
    _fields_ = [('ErrCode', c_uint),
                ('Passive_ErrData', c_byte * 3),
                ('ArLost_ErrData', c_byte), ]


class MyWindow(QMainWindow, Ui_BMU_CANTOOL):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('BMU_CANTool   V.1.0.1  平旦科技')
        self.label_OnlineFlag.setText('离线状态')

        # 监听按钮事件
        self.pushButton_CANConnect.clicked.connect(self.CAN_Open)
        self.pushButton_SaverInfo.clicked.connect(self.CellInfoSave)
        self.checkBox_AutoRead.stateChanged.connect(self.CellInfoRead)
        self.pushButton_ClearInfo.clicked.connect(self.CellInfoclear)
        self.pushButton_StandVol.clicked.connect(self.StandVolData)
        self.pushButton_ReviewSystem.clicked.connect(self.ReviewSystem)
        self.pushButton_ReadPara.clicked.connect(self.ReadSystemPara)
        self.pushButton_WritePara.clicked.connect(self.SetSystemPara)
        self.pushButton_Balance.clicked.connect(self.BalanceSend)
        self.checkBox_ReadAllPara.stateChanged.connect(self.ReadParaAll)
        self.checkBox_SetAllPara.stateChanged.connect(self.SetParaAll)

        # self.checkBox_Balance_1.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_2.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_3.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_4.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_5.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_6.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_7.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_8.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_9.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_10.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_11.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_12.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_13.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_14.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_15.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_16.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_17.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_18.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_19.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_20.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_21.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_22.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_23.stateChanged.connect(self.BalanceSend)
        # self.checkBox_Balance_24.stateChanged.connect(self.BalanceSend)
        self.checkBox_BananceAll.stateChanged.connect(self.BalanceChoceAll)
        self.comboBox_BMUNum.currentIndexChanged.connect(self.SetBMUNum)



        Data_RefreshTimer.timeout.connect(self.VolBalance_TimeOut)
        Data_QueryTimer.timeout.connect(self.DataQuery_TimeOut)






    n = 0

    # 打开设备按钮
    def CAN_Open(self):
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        global CANDeviceBoundRate
        global Path
        global BMU_Index
        # self.label_OnlineFlag
        print(self.pushButton_CANConnect.text())
        '''
        tem = 'FFFC'
        a = bin(int(tem,16))[2:]
        b = -int(DataTurn.reverse_func(a),2)/10-40
        print(a)
        print(b)
        '''


        if self.pushButton_CANConnect.text() == '打开设备':
            CANOpen = BMU_CANCOMDEAL.CAN_Open(self)
            # CANOpen =BMU_CANCOM.CAN_Init(self,Path)
            print('CANOpen=' + str(CANOpen))
            if CANOpen == 1:
                self.comboBox_CANChannel.setEnabled(False)
                self.comboBox_CANIndex.setEnabled(False)
                self.comboBox_CANBoundRate.setEnabled(False)
                self.comboBox_CANDevice.setEnabled(False)
                self.pushButton_CANConnect.setText("关闭设备")
                self.label_OnlineFlag.setText('在线状态')
                BMU_Index = self.comboBox_BMUNum.currentIndex()

        elif self.pushButton_CANConnect.text() == '关闭设备':
            # 关闭自动读数
            self.checkBox_AutoRead.setCheckState(0)
            CANClose = BMU_CANCOMDEAL.CAN_Close(self)
            print('CANClose=' + str(CANClose))
            if CANClose == 1:
                self.comboBox_CANChannel.setEnabled(True)
                self.comboBox_CANIndex.setEnabled(True)
                self.comboBox_CANBoundRate.setEnabled(True)
                self.comboBox_CANDevice.setEnabled(True)
                self.pushButton_CANConnect.setText("打开设备")
                self.label_OnlineFlag.setText('离线状态')

        # 读取版本号
        self.ReadVersion()

        return 1


    # 发送数据方法
    def Data_Send(self):
        if self.label_OnlineFlag.text() == '在线状态':
            # 写入基准电压
            self.SendVolData()

            return 1
        else:
            QMessageBox.warning(self, "提示", "请先启动CAN！", QMessageBox.Yes)
            return 0

        # BMU_CANCOM_Test.CAN_Open(self,Path)
        # 创建子线程
        # t1 = threading.Thread(target=BMU_CANCOM_Test.CAN_SendData(self,Path), args=(6,))
        # 守护线程 setDaemon()  语法：子线程名.setDaemon()
        # 主线程执行完，子线程也跟着结束，默认False，要True
        # t1.setDaemon(True)
        # 开启子线程  start()
        # t1.start()
        # print(t1.getName())
        # BMU_CANCOM_Test.CAN_SendData(self,DataVol)
        # BMU_CANCOM_Test.CAN_ReciveData(self)

    # 读取excel电压值
    def CellInfoRead(self):
        # 打开excel文件
        # 打开excel文件
        path = 'Cell_Power.xlsx'
        if self.label_OnlineFlag.text() == '在线状态':
            if self.checkBox_AutoRead.isChecked() == True:
                # 设置定500ms的时器，每5秒读取一次
                # Data_RefreshTimer.start(500)
                # print("读取文件")
                PythonMemory.read_excel_qt(self.tableWidget_CellInfo, path)

                self.ReadVolData()

                self.ReadTempData()
                # 开启定时读取
                Data_QueryTimer.start(1000)
            else:
                Data_QueryTimer.stop()
                self.checkBox_AutoRead.setCheckState(0)
                return 0
                # Data_RefreshTimer.stop()
            return 1
        else:

            return 0




    def DataQuery_TimeOut(self):
        # 打开excel文件
        print("定时读取")
        if self.label_OnlineFlag.text() == '在线状态':
            if self.checkBox_AutoRead.isChecked() == True:

                self.ReadVolData()
                time.sleep(0.4)
                self.ReadTempData()
                # 获取tableWidget的行列数
                row = self.tableWidget_CellInfo.rowCount()

                for i in range(row):
                    # tableWidget.insertRow(row)
                    try:
                        # 阈值
                        m = self.lineEdit_Threshold.text()
                        if m=='' or m == None:
                            m=0

                        # 计算实际电压和基准电压的差值

                        n =  int(self.tableWidget_CellInfo.item(i,0).text())- int(self.tableWidget_CellInfo.item(i,1).text())
                        a = abs(n)
                        # print(str(n))
                        newItem = QTableWidgetItem(str(abs(n)))
                        # 如果差值大于阈值，则将差值字体设置为红色
                        try:
                            if (a >= int(m) and m!=0):
                                newItem.setForeground(QBrush(QColor(255, 0, 0)))
                        except:
                            print("阈值为0")
                            return 1

                        # print("\033[31m这是红色字体\033[0m")
                        # print(str(rowslist[j]))
                        self.tableWidget_CellInfo.setItem(i,2 , newItem)

                    except:
                        print('读取失败')

            else:
                return 0
                # Data_RefreshTimer.stop()
            return 1
        else:
            Data_QueryTimer.stop()
            QMessageBox.warning(self, "提示", "请先启动设备！", QMessageBox.Yes)
            return 0

        # 如果自动读取被选中则读取数据否则删除
        # if self.checkBox_AutoRead.isChecked()==True:
            # print("读取文件")
            # PythonMemory.read_excel_qt(self.tableWidget_CellInfo, path)
        # else:
            # PythonMemory.cleartableWidget(self.tableWidget_CellInfo)

        # print(self.checkBox_AutoRead.)

    # 将电压值保存至excel文件
    def CellInfoSave(self):
        # 打开excel文件
        path = 'Cell_Power.xlsx'

        if (self.tableWidget_CellInfo.item(1, 1)==None):
            QMessageBox.warning(self, "提示", "数据为空", QMessageBox.Yes)
            return 0
        else:
            # 获取电压差值阈值
            m = self.lineEdit_Threshold.text()
            # print("读取文件") 二次保存确保数据保存
            PythonMemory.write_qt_excel(self.tableWidget_CellInfo, path, m)
            PythonMemory.write_qt_excel(self.tableWidget_CellInfo, path, m)
            print('已保存至excel')
            # 下设基准电压
            Recive_Data = self.SendVolData()
            print('Recive_Data1=', Recive_Data)
            self.textBrowser_Info.append('电压基准值写入:')
            self.textBrowser_Info.append(str(Recive_Data))
            return 1


    # 清除数据
    def CellInfoclear(self):
        if self.checkBox_AutoRead.isChecked():
            QMessageBox.warning(self, "提示", "请先关闭自动读取！", QMessageBox.Yes)
            return 0
        self.tableWidget_CellInfo.item(1,1)
        print('清除数据')
        PythonMemory.cleartableWidget(self.tableWidget_CellInfo)
        self.textBrowser_Info.setText('')

    # 写入基准电压
    def SendVolData(self):
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        global CANDeviceBoundRate
        global thread2
        # BMS_ID= 0x18076564
        BMU_ID = 0x180F6564
        Data = (0, 0, 0, 0, 0, 0, 0, 0)
        Data = (0x01, 0x01, 0x2C, 0x02, 0x0C, 0xA1, 0x0C, 0x9B)
        rowCount = self.tableWidget_CellInfo.rowCount()

        DataVol = []
        Adress = []

        # 两组电池一个地址
        for j in range(rowCount // 2):
            # upper()转换成大写，两个lstrip()将"0X"删除,zfill()填充两位
            # upper().lstrip("0").lstrip("X").zfill(2)

            Adress16 = DataTurn.DecToHex(300 + j * 2).upper().lstrip("0").lstrip("X").zfill(2)
            Adress16 = '0' + str(Adress16)
            Adress.append(int(Adress16[0:2], 16))
            Adress.append(int(Adress16[2:4], 16))
            # print('Adress16=',Adress16)

            # Adress.append(DataTurn.DecToHex(300 + j*2).upper().lstrip("0").lstrip("X").zfill(2))

        for i in range(rowCount):
            # DataVol.append(int(self.tableWidget_CellInfo.item(i,1).text()))
            DataVol16 = DataTurn.DecToHex(self.tableWidget_CellInfo.item(i, 1).text()).upper().lstrip("0").lstrip("X")
            print(DataVol16)
            # print('len=',len(DataVol16))
            if len(DataVol16) == 3:
                DataVol16 = '0' + str(DataVol16)
            elif len(DataVol16) == 2:
                DataVol16 = '00' + str(DataVol16)
            elif len(DataVol16) == 1:
                DataVol16 = '000' + str(DataVol16)
            else:
                DataVol16 = '0000'

            DataVol.append(int(DataVol16[0:2], 16))
            DataVol.append(int(DataVol16[2:4], 16))

        print('DataVol=', DataVol)

        # Temp_Data=(0x01, DataVol[1], DataVol[2], 0x02, DataVol[4], DataVol[5], DataVol[6], DataVol[7])
        # time.sleep(0.01)
        # 循环写入基准电压
        Send_Data1 = (0x01, 0x01, 0x2C, 0x02, 0x0D, 0x02, 0x0D, 0x02)
        Send_Data2 = (0x01, 0x01, 0x2E, 0x02, 0x0D, 0x02, 0x0D, 0x02)
        # print('Send_Data1=', Send_Data1)
        # print('Send_Data1=', Send_Data2)
        # print('rowCount=',rowCount)
        BMU_CANCOMDEAL.CAN_ClearBuffer(self)
        for m in range(rowCount // 2):
            print(m, '基准电压地址=', Adress[m])
            Send_Data = (0x01, Adress[m * 2], Adress[m * 2 + 1], 0x02, DataVol[m * 4], DataVol[m * 4 + 1], DataVol[m * 4 + 2], DataVol[m * 4 + 3])
            print('Send_Data=',Send_Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Send_Data)
            # time.sleep(0.02)
            # BMU_CANCOM_Test.CAN_ReciveData(self)

        Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))

        # BMU_CANCOM_Test.CAN_SendData(self, Send_Data1)
        # BMU_CANCOM_Test.CAN_ReciveData(self)

        return Recive_Data

    # 校准电压
    def StandVolData(self):
        try:
            if self.checkBox_AutoRead.isChecked():
                QMessageBox.warning(self, "提示", "请先关闭自动读取！", QMessageBox.Yes)
                return
            if self.label_OnlineFlag.text() == '在线状态':
                BMU_ID = 0x180F6564
                print('校准电压')
                Data = (0x01, 0x00, 0xE6, 0x01, 0x00, 0x01, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)
                if str(Recive_Data[0])[0:6] == '0x188f':


                    if (Recive_Data[1] == '0100E60100010000'):

                        self.textBrowser_Info.append('下设成功\n')
                    else:
                        self.textBrowser_Info.append('下设失败\n')
                    return 1
            else:
                QMessageBox.warning(self, "提示", "请先启动设备！", QMessageBox.Yes)
                return 0
        except:
            pass

    # 读取实际电压值
    def ReadVolData(self):
        try:
            if self.label_OnlineFlag.text() == '在线状态':
                # BMS_ID = 0x180F6564
                BMU_ID = 0x18016564
                print('实际电压电压')
                Data = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
                # print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                ReciveVolData = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                if str(ReciveVolData[0][0:6]) == '0x1881':
                    # print('-----------------------------------------------')
                    # 将读取到的电压写入VolCell数组中
                    VolCell = []
                    DataLen = len(ReciveVolData)
                    CellLen = (DataLen-1) * 3

                    str3 = int(str(ReciveVolData[0])[4:8],16)
                    # print('str3',str3)
                    for i in range(DataLen-1):
                        VolCell.append(int(str(ReciveVolData[i+1])[4:8],16))
                        VolCell.append(int(str(ReciveVolData[i+1])[8:12],16))
                        VolCell.append(int(str(ReciveVolData[i+1])[12:16],16))



                    # 将VolCell数组中的数据写入tableWidget_CellInfo
                    # print('CellLen=',CellLen)
                    for m in range(CellLen):
                        # 把数据写入tablewidget中
                        newItem = QTableWidgetItem(str(VolCell[m]))
                        # print(str(rowslist[j]))
                        self.tableWidget_CellInfo.setItem(m, 0, newItem)

                    rownum = self.tableWidget_CellInfo.rowCount()
                    tableWidget_Vol = []
                    for i in range(rownum):
                        if self.tableWidget_CellInfo.item(i, 0).text() != None and self.tableWidget_CellInfo.item(i,
                                                                                                                  0).text() != '':
                            tableWidget_Vol.append(int(self.tableWidget_CellInfo.item(i, 0).text()))


                    # 求出实际最大电压和最小电压
                    min_volindex, min_volnumber = min(enumerate(tableWidget_Vol), key=operator.itemgetter(1))
                    # print('实际最小电压')
                    # print('VolCell', str(VolCell))
                    self.lineEdit_MinVol.setText(str(min_volnumber))
                    self.lineEdit_MinVolNum.setText(str(min_volindex + 1))

                    max_index, max_number = max(enumerate(tableWidget_Vol), key=operator.itemgetter(1))
                    self.lineEdit_MaxVol.setText(str(max_number))
                    self.lineEdit_MaxVolNum.setText(str(max_index + 1))
                    # self.textBrowser_Info.append(str(tableWidget_Vol))
                    print('实际电压读取完成')

                return 1
            else:
                # QMessageBox.warning(self, "提示", "请先启动CAN！", QMessageBox.Yes)
                return 0
        except:
            pass

    # 读取实际温度
    def ReadTempData(self):
        if self.label_OnlineFlag.text() == '在线状态':
            # BMS_ID = 0x180F6564
            try:
                BMU_ID = 0x18026564
                Data = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
                print('实际温度Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                # print('Recive_Data=', Recive_Data)
                if str(Recive_Data[0])[0:6] == '0x1882':
                    # 将读取到的温度写入TempCell数组中
                    TempCell = []

                    DataLen = len(Recive_Data)
                    CellLen = (DataLen-1) * 3
                    str3 = int(str(Recive_Data[0])[4:8],16)
                    # print('str3',str3)
                    for i in range(DataLen-1):
                        TempCell.append(int(str(Recive_Data[i + 1])[0:4], 16))
                        # print('-----------------------------------')

                        if int(str(Recive_Data[i+1])[4:8],16)>0xFF00:
                            tem = str(Recive_Data[i+1])[4:8]
                            # 转换为二进制字符串
                            a = bin(int(tem, 16))[2:]
                            # 取反
                            b = -int(DataTurn.reverse_func(a), 2) / 10 - 40
                            TempCell.append(b)
                        else:
                            TempCell.append((int(str(Recive_Data[i + 1])[4:8], 16)-400)/10)

                        if int(str(Recive_Data[i+1])[8:12],16)>0xFF00:
                            tem = str(Recive_Data[i + 1])[8:12]
                            a = bin(int(tem, 16))[2:]
                            b = -int(DataTurn.reverse_func(a), 2) / 10 - 40
                            TempCell.append(b)
                        else:
                            TempCell.append((int(str(Recive_Data[i + 1])[8:12], 16)-400)/10)

                        if int(str(Recive_Data[i+1])[12:16],16)>0xFF00:
                            tem = str(Recive_Data[i + 1])[12:16]
                            a = bin(int(tem, 16))[2:]
                            b = -int(DataTurn.reverse_func(a), 2) / 10 - 40
                            TempCell.append(b)
                        else:
                            TempCell.append((int(str(Recive_Data[i + 1])[12:16], 16)-400)/10)

                    # self.textBrowser_Info.append(str(TempCell))

                    # 将VolCell数组中的数据写入tableWidget_CellInfo
                    # print('*************TempCell***********',TempCell)
                    self.textBrowser_Info.append(str(TempCell))
                    for m in range(30):
                        if m ==0 or m ==4 or m ==8 or m ==12 or m ==16 or m ==20 or m ==24 or m ==28:
                            try:
                                j = int(TempCell[m])
                                # print('j=',j)

                                # TempCell[m+1] = (TempCell[m+1] - 400)/10

                                # 把数据写入tablewidget中
                                newItem = QTableWidgetItem(str(TempCell[m+1]))
                                # print(str(rowslist[j]))
                                self.tableWidget_CellInfo.setItem(j-1, 3, newItem)

                                # TempCell[m+2] = (TempCell[m + 2] - 400)/10

                                newItem = QTableWidgetItem(str(TempCell[m+2]))
                                self.tableWidget_CellInfo.setItem(j, 3, newItem)

                                # TempCell[m + 3] = (TempCell[m + 3] - 400)/10

                                newItem = QTableWidgetItem(str(TempCell[m + 3]))
                                self.tableWidget_CellInfo.setItem(j+1, 3, newItem)
                            except:
                                continue

                rownum = self.tableWidget_CellInfo.rowCount()
                tableWidget_Temp = []
                for i in range(rownum):
                    if self.tableWidget_CellInfo.item(i,3).text() != None and self.tableWidget_CellInfo.item(i,3).text()!='':
                        tableWidget_Temp.append(float(self.tableWidget_CellInfo.item(i,3).text()))
                # print('tableWidget_Temp',tableWidget_Temp)
                max_index, max_number = max(enumerate(tableWidget_Temp), key=operator.itemgetter(1))
                self.lineEdit_MaxTemp.setText(str(max_number))
                self.lineEdit_MaxTempNum.setText(str(max_index + 1))

                min_index, min_number = min(enumerate(tableWidget_Temp), key=operator.itemgetter(1))
                # print('实际最小温度')

                self.lineEdit_MinTemp.setText(str(min_number))
                self.lineEdit_MinTempNum.setText(str(min_index + 1))
                self.textBrowser_Info.append(str(tableWidget_Temp))

                print('实际温度读取完成')

                return 1
            except:
                print('温度读取出错')
                return 0
        else:
            QMessageBox.warning(self, "提示", "请先启动CAN！", QMessageBox.Yes)
            return 0


    # 读取版本号
    def ReadVersion(self):
        global BMU_Index
        if self.label_OnlineFlag.text() == '在线状态':
            try:
                BMU_ID = 0x18076564
                print('读取版本号')
                Data = (0x01, 0x00, 0xE6, 0x01, 0x00, 0x01, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self,BMU_ID ,Data)
                time.sleep(1)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)

                if str(Recive_Data[0])[0:6] == '0x1887':
                    BMU_Version = Recive_Data[1][12:16]

                    BMU_Version = str(int(BMU_Version, 16))
                    a = '.'
                    BMU_Version = a.join(BMU_Version)
                # VersionTitle = 'BMU-V'+ BMU_Version + '   平旦科技'
                # self.setWindowTitle(VersionTitle)
                # self.textBrowser_Info.append('V'+BMU_Version)

                self.label_Ver.setText('V'+BMU_Version)
            except:
                print('读取错误')
                return 0
        else:
            self.setWindowTitle('BMU_CANTool   V.1.0.1  平旦科技')
            return 0

    # 系统复位
    def ReviewSystem(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('系统复位')
            Data = (0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self,BMU_ID ,Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textBrowser_Info.append('系统复位\n')
        else:
            return 0

    # 设置系统参数
    def SetSystemPara(self):
        if self.label_OnlineFlag.text() == '离线状态':
            return 0
        time.sleep(0.5)
        row = self.tableWidget_Para.rowCount()
        print('设置系统参数')
        for i in range(row):
            # 模块地址
            if i == 1:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetBMUAdress(self)
            # 电压个数写入
            if i == 2:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetVolNum(self)
            # 温度个数
            if i == 3:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempNum(self)
            # 电压K值
            if i == 4:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetVolKNum(self)
            # 电压B值
            if i == 5:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempBNum(self)
            # 设置温度总K值(K1)
            if i == 6:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempK_One(self)
            # 设置温度总B值(B1)
            if i == 7:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempB_One(self)
            # 设置温度总K值(K2)
            if i == 8:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempK_Two(self)
            # 设置温度总B值(B2)
            if i == 9:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempB_Two(self)
            # 设置温度的Bx值
            if i == 10:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetTempBx(self)
                    # print(Recive_Data[0])
            # 设置NTC的阻值
            if i == 11:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.SetNTC(self)
                    # print(Recive_Data[0])
            # DO控制合
            if i == 12:
                if str(self.tableWidget_Para.item(i, 3).text()) == '1':
                    Recive_Data = BMU_CANPARASET.DOControlOn(self)
                    # print(Recive_Data[0])
        self.textEdit_Para.append('写入完成')


        return 1

    # 读取系统参数
    def ReadSystemPara(self):
        if self.label_OnlineFlag.text() == '离线状态':
            return 0
        time.sleep(0.5)
        row = self.tableWidget_Para.rowCount()
        for i in range(row):
            # 读取模块地址
            if i == 1:
                if str(self.tableWidget_Para.item(i, 2).text()) == '1':
                    Recive_Data = BMU_CANPARASET.BMUAdress(self)
                    if Recive_Data[0][0:6] == '0x188f':
                        TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12], 16)))
                        self.tableWidget_Para.setItem(i, 0, TempBxItem)
                    else:
                        pass

            # 读取电压个数
            if i == 2:
                if str(self.tableWidget_Para.item(i, 2).text()) == '1':
                    Recive_Data = BMU_CANPARASET.VolNum(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12], 16)))
                    self.tableWidget_Para.setItem(i, 0, TempBxItem)

            # 读取温度个数
            if i == 3:
                if str(self.tableWidget_Para.item(i, 2).text()) == '1':
                    Recive_Data = BMU_CANPARASET.TempNum(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12], 16)))
                    self.tableWidget_Para.setItem(i, 0, TempBxItem)

            # 读取电压K值
            if i == 4:
                if str(self.tableWidget_Para.item(i, 2).text()) == '1':
                    Recive_Data = BMU_CANPARASET.VolKNum(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12], 16)))
                    self.tableWidget_Para.setItem(i, 0, TempBxItem)

            # 读取电压B值
            if i == 5:
                if str(self.tableWidget_Para.item(i, 2).text()) == '1':
                    Recive_Data = BMU_CANPARASET.TempBNum(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12], 16)))
                    self.tableWidget_Para.setItem(i, 0, TempBxItem)

            # 读取温度总K值(K1)
            if i == 6:
                # print(self.tableWidget_Para.item(i,2).text())
                if str(self.tableWidget_Para.item(i,2).text()) =='1':
                    Recive_Data = BMU_CANPARASET.ReadTempK_One(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12],16)))
                    self.tableWidget_Para.setItem(i,0,TempBxItem)

            # 读取温度总B值(B1)
            if i == 7:
                # print(self.tableWidget_Para.item(i,2).text())
                if str(self.tableWidget_Para.item(i,2).text()) =='1':
                    Recive_Data = BMU_CANPARASET.ReadTempB_One(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12],16)))
                    self.tableWidget_Para.setItem(i,0,TempBxItem)

            # 读取温度总K值(K2)
            if i == 8:
                # print(self.tableWidget_Para.item(i,2).text())
                if str(self.tableWidget_Para.item(i,2).text()) =='1':
                    Recive_Data = BMU_CANPARASET.ReadTempK_Two(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12],16)))
                    self.tableWidget_Para.setItem(i,0,TempBxItem)

            # 读取温度总B值(B2)
            if i == 9:
                # print(self.tableWidget_Para.item(i,2).text())
                if str(self.tableWidget_Para.item(i,2).text()) =='1':
                    Recive_Data = BMU_CANPARASET.ReadTempB_Two(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12],16)))
                    self.tableWidget_Para.setItem(i,0,TempBxItem)

            # 读取温度的Bx值
            if i == 10:
                # print(self.tableWidget_Para.item(i,2).text())
                if str(self.tableWidget_Para.item(i,2).text()) =='1':
                    Recive_Data = BMU_CANPARASET.ReadTempBx(self)
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12],16)))
                    self.tableWidget_Para.setItem(i,0,TempBxItem)
            # 读取NTC的阻值
            if i == 11:
                # print(self.tableWidget_Para.item(i,2).text())
                if str(self.tableWidget_Para.item(i,2).text()) =='1':
                    Recive_Data = BMU_CANPARASET.ReadNTC(self)
                    # print(Recive_Data[0][8:12])
                    TempBxItem = QTableWidgetItem(str(int(Recive_Data[1][8:12],16)))
                    self.tableWidget_Para.setItem(i,0,TempBxItem)

            # DO控制分
            if i == 12:
                if str(self.tableWidget_Para.item(i, 2).text()) == '1':
                    Recive_Data = BMU_CANPARASET.DOControlOff(self)

                    # print(Recive_Data[0])
        self.textEdit_Para.append('读取完成')
        return 1

    # 系统参数读取全部设置为1
    def ReadParaAll(self):
        if (self.checkBox_ReadAllPara.isChecked()):
            BMU_CANPARASET.ReadAll(self.tableWidget_Para)
        else:
            BMU_CANPARASET.ReadNone(self.tableWidget_Para)
        return 1

    # 系统参数写入全部设置为1
    def SetParaAll(self):
        if (self.checkBox_SetAllPara.isChecked()):
            BMU_CANPARASET.SetAll(self.tableWidget_Para)
        else:
            BMU_CANPARASET.SetNone(self.tableWidget_Para)
        return 1

    # 均衡控制定时器任务
    def VolBalance_TimeOut(self):
        try:
            BMU_ID = 0x180A6564
            Data = (0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            # 返回参数：是否已经开启被动均衡
            IsBalance = False
            CellBalance = str(Recive_Data[1][0:2])
            # 将数据帧按高低位转换为二进制放入数组中
            Cell = []
            Cellstr_1 = str(bin(int((Recive_Data[1][11:12]),16))[2:].zfill(4))
            Cell.append(Cellstr_1[3:4])
            Cell.append(Cellstr_1[2:3])
            Cell.append(Cellstr_1[1:2])
            Cell.append(Cellstr_1[0:1])

            Cellstr_10 = str(bin(int((Recive_Data[1][10:11]),16))[2:].zfill(4))
            Cell.append(Cellstr_10[3:4])
            Cell.append(Cellstr_10[2:3])
            Cell.append(Cellstr_10[1:2])
            Cell.append(Cellstr_10[0:1])

            Cellstr_2 = str(bin(int((Recive_Data[1][9:10]), 16))[2:].zfill(4))
            Cell.append(Cellstr_2[3:4])
            Cell.append(Cellstr_2[2:3])
            Cell.append(Cellstr_2[1:2])
            Cell.append(Cellstr_2[0:1])
            Cellstr_20 = str(bin(int((Recive_Data[1][8:9]), 16))[2:].zfill(4))
            Cell.append(Cellstr_20[3:4])
            Cell.append(Cellstr_20[2:3])
            Cell.append(Cellstr_20[1:2])
            Cell.append(Cellstr_20[0:1])
            Cellstr_3 = str(bin(int((Recive_Data[1][15:16]), 16))[2:].zfill(4))
            Cell.append(Cellstr_3[3:4])
            Cell.append(Cellstr_3[2:3])
            Cell.append(Cellstr_3[1:2])
            Cell.append(Cellstr_3[0:1])
            Cellstr_30 = str(bin(int((Recive_Data[1][14:15]), 16))[2:].zfill(4))
            Cell.append(Cellstr_30[3:4])
            Cell.append(Cellstr_30[2:3])
            Cell.append(Cellstr_30[1:2])
            Cell.append(Cellstr_30[0:1])
            # print('Cellstr_1',Cellstr_1)
            # print('Cellstr_10',Cellstr_10)

            # print('Cell',Cell)
            # 根据返回帧数据解析
            numBalance = 0
            for i in range(24):
                if (i == 0 and Cell[i] == '0'):
                    self.checkBox_Balance_1.setCheckState(0)
                if (i == 0 and Cell[i] == '1'):
                    self.checkBox_Balance_1.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 1 and Cell[i] == '0'):
                    self.checkBox_Balance_2.setCheckState(0)
                if (i == 1 and Cell[i] == '1'):
                    self.checkBox_Balance_2.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 2 and Cell[i] == '0'):
                    self.checkBox_Balance_3.setCheckState(0)
                if (i == 2 and Cell[i] == '1'):
                    self.checkBox_Balance_3.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 3 and Cell[i] == '0'):
                    self.checkBox_Balance_4.setCheckState(0)
                if (i == 3 and Cell[i] == '1'):
                    self.checkBox_Balance_4.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 4 and Cell[i] == '0'):
                    self.checkBox_Balance_5.setCheckState(0)
                if (i == 4 and Cell[i] == '1'):
                    self.checkBox_Balance_5.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 5 and Cell[i] == '0'):
                    self.checkBox_Balance_6.setCheckState(0)
                if (i == 5 and Cell[i] == '1'):
                    self.checkBox_Balance_6.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 6 and Cell[i] == '0'):
                    self.checkBox_Balance_7.setCheckState(0)
                if (i == 6 and Cell[i] == '1'):
                    self.checkBox_Balance_7.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 7 and Cell[i] == '0'):
                    self.checkBox_Balance_8.setCheckState(0)
                if (i == 7 and Cell[i] == '1'):
                    self.checkBox_Balance_8.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 8 and Cell[i] == '0'):
                    self.checkBox_Balance_9.setCheckState(0)
                if (i == 8 and Cell[i] == '1'):
                    self.checkBox_Balance_9.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 9 and Cell[i] == '0'):
                    self.checkBox_Balance_10.setCheckState(0)
                if (i == 9 and Cell[i] == '1'):
                    self.checkBox_Balance_10.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 10 and Cell[i] == '0'):
                    self.checkBox_Balance_11.setCheckState(0)
                if (i == 10 and Cell[i] == '1'):
                    self.checkBox_Balance_11.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 11 and Cell[i] == '0'):
                    self.checkBox_Balance_12.setCheckState(0)
                if (i == 11 and Cell[i] == '1'):
                    self.checkBox_Balance_12.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 12 and Cell[i] == '0'):
                    self.checkBox_Balance_13.setCheckState(0)
                if (i == 12 and Cell[i] == '1'):
                    self.checkBox_Balance_13.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 13 and Cell[i] == '0'):
                    self.checkBox_Balance_14.setCheckState(0)
                if (i == 13 and Cell[i] == '1'):
                    self.checkBox_Balance_14.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 14 and Cell[i] == '0'):
                    self.checkBox_Balance_15.setCheckState(0)
                if (i == 14 and Cell[i] == '1'):
                    self.checkBox_Balance_15.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 15 and Cell[i] == '0'):
                    self.checkBox_Balance_16.setCheckState(0)
                if (i == 15 and Cell[i] == '1'):
                    self.checkBox_Balance_16.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 16 and Cell[i] == '0'):
                    self.checkBox_Balance_17.setCheckState(0)
                if (i == 16 and Cell[i] == '1'):
                    self.checkBox_Balance_17.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 17 and Cell[i] == '0'):
                    self.checkBox_Balance_18.setCheckState(0)
                if (i == 17 and Cell[i] == '1'):
                    self.checkBox_Balance_18.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 18 and Cell[i] == '0'):
                    self.checkBox_Balance_19.setCheckState(0)
                if (i == 18 and Cell[i] == '1'):
                    self.checkBox_Balance_19.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 19 and Cell[i] == '0'):
                    self.checkBox_Balance_20.setCheckState(0)
                if (i == 19 and Cell[i] == '1'):
                    self.checkBox_Balance_20.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 20 and Cell[i] == '0'):
                    self.checkBox_Balance_21.setCheckState(0)
                if (i == 20 and Cell[i] == '1'):
                    self.checkBox_Balance_21.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 21 and Cell[i] == '0'):
                    self.checkBox_Balance_22.setCheckState(0)
                if (i == 21 and Cell[i] == '1'):
                    self.checkBox_Balance_22.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 22 and Cell[i] == '0'):
                    self.checkBox_Balance_23.setCheckState(0)
                if (i == 22 and Cell[i] == '1'):
                    self.checkBox_Balance_23.setCheckState(1)
                    numBalance = numBalance + 1
                if (i == 23 and Cell[i] == '0'):
                    self.checkBox_Balance_24.setCheckState(0)
                if (i == 23 and Cell[i] == '1'):
                    self.checkBox_Balance_24.setCheckState(1)
                    numBalance = numBalance + 1

                self.label_BananceTip.setText(str(numBalance)+'被动均衡')

            # 如果无均衡则停止计时器
            if CellBalance == '00':
                Data_RefreshTimer.stop()

                self.checkBox_BananceAll.setCheckState(0)
                self.BalanceChoceNone()
                IsBalance = False
            else:
                IsBalance = True
            return  IsBalance
        except:
            self.checkBox_BananceAll.setCheckState(0)
            self.BalanceChoceNone()
            pass

    # 被动均衡控制
    def CheckVolBalance(self):
        try:
            if self.label_OnlineFlag.text() == '离线状态':
                QMessageBox.warning(self, "提示", "请打开设备!", QMessageBox.Yes)
                return 0
            CellBalance = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            if self.checkBox_Balance_1.checkState()== 2 or self.checkBox_Balance_1.checkState()== 1:
                CellBalance[15] = 1
            else:
                CellBalance[15] = 0

            if self.checkBox_Balance_2.checkState()== 2 or self.checkBox_Balance_2.checkState()== 1:
                CellBalance[14] = 1
            else:
                CellBalance[14] = 0

            if self.checkBox_Balance_3.checkState()== 2 or self.checkBox_Balance_3.checkState()== 1:
                CellBalance[13] = 1
            else:
                CellBalance[13] = 0

            if self.checkBox_Balance_4.checkState()== 2 or self.checkBox_Balance_4.checkState()== 1:
                CellBalance[12] = 1
            else:
                CellBalance[12] = 0

            if self.checkBox_Balance_5.checkState() == 2 or self.checkBox_Balance_5.checkState() == 1:
                CellBalance[11] = 1
            else:
                CellBalance[11] = 0

            if self.checkBox_Balance_6.checkState() == 2 or self.checkBox_Balance_6.checkState() == 1:
                CellBalance[10] = 1
            else:
                CellBalance[10] = 0

            if self.checkBox_Balance_7.checkState() == 2 or self.checkBox_Balance_7.checkState() == 1:
                CellBalance[9] = 1
            else:
                CellBalance[9] = 0

            if self.checkBox_Balance_8.checkState() == 2 or self.checkBox_Balance_8.checkState() == 1:
                CellBalance[8] = 1
            else:
                CellBalance[8] = 0

            if self.checkBox_Balance_9.checkState() == 2 or self.checkBox_Balance_9.checkState() == 1:
                CellBalance[7] = 1
            else:
                CellBalance[7] = 0

            if self.checkBox_Balance_10.checkState() == 2 or self.checkBox_Balance_10.checkState() == 1:
                CellBalance[6] = 1
            else:
                CellBalance[6] = 0

            if self.checkBox_Balance_11.checkState() == 2 or self.checkBox_Balance_11.checkState() == 1:
                CellBalance[5] = 1
            else:
                CellBalance[5] = 0

            if self.checkBox_Balance_12.checkState() == 2 or self.checkBox_Balance_12.checkState() == 1:
                CellBalance[4] = 1
            else:
                CellBalance[4] = 0

            if self.checkBox_Balance_13.checkState() == 2 or self.checkBox_Balance_13.checkState() == 1:
                CellBalance[3] = 1
            else:
                CellBalance[3] = 0

            if self.checkBox_Balance_14.checkState() == 2 or self.checkBox_Balance_14.checkState() == 1:
                CellBalance[2] = 1
            else:
                CellBalance[2] = 0

            if self.checkBox_Balance_15.checkState() == 2 or self.checkBox_Balance_15.checkState() == 1:
                CellBalance[1] = 1
            else:
                CellBalance[1] = 0

            if self.checkBox_Balance_16.checkState() == 2 or self.checkBox_Balance_16.checkState() == 1:
                CellBalance[0] = 1
            else:
                CellBalance[0] = 0

            if self.checkBox_Balance_17.checkState() == 2 or self.checkBox_Balance_17.checkState() == 1:
                CellBalance[31] = 1
            else:
                CellBalance[31] = 0

            if self.checkBox_Balance_18.checkState() == 2 or self.checkBox_Balance_18.checkState() == 1:
                CellBalance[30] = 1
            else:
                CellBalance[30] = 0

            if self.checkBox_Balance_19.checkState() == 2 or self.checkBox_Balance_19.checkState() == 1:
                CellBalance[29] = 1
            else:
                CellBalance[29] = 0

            if self.checkBox_Balance_20.checkState() == 2 or self.checkBox_Balance_20.checkState() == 1:
                CellBalance[28] = 1
            else:
                CellBalance[28] = 0

            if self.checkBox_Balance_21.checkState() == 2 or self.checkBox_Balance_21.checkState() == 1:
                CellBalance[27] = 1
            else:
                CellBalance[27] = 0

            if self.checkBox_Balance_22.checkState() == 2 or self.checkBox_Balance_22.checkState() == 1:
                CellBalance[26] = 1
            else:
                CellBalance[26] = 0

            if self.checkBox_Balance_23.checkState() == 2 or self.checkBox_Balance_23.checkState() == 1:
                CellBalance[25] = 1
            else:
                CellBalance[25] = 0

            if self.checkBox_Balance_24.checkState() == 2 or self.checkBox_Balance_24.checkState() == 1:
                CellBalance[24] = 1
            else:
                CellBalance[24] = 0

            strCell = ''
            for i in range(len(CellBalance)):
                strCell = strCell + str(CellBalance[i])

            Datat = DataTurn.sep_four(strCell)
            Datas = []
            Datas.append(str(Datat[0])+str(Datat[1]))
            Datas.append(str(Datat[2]) + str(Datat[3]))
            Datas.append(str(Datat[4]) + str(Datat[5]))
            Datas.append(str(Datat[6]) + str(Datat[7]))

            print('CellBalance==',strCell)
            print(Datas)
            Data = (0x01, 0x02, 0x00, 0x00, int(Datas[0],16), int(Datas[1],16), int(Datas[2],16), int(Datas[3],16))
            # print(Data)

                # Data = (0x01, 0x02, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0xFF)
            return Data
        except:
            QMessageBox.warning(self, "提示", "错误", QMessageBox.Yes)
    # 均衡下设
    def BalanceSend(self):
        # 全部均衡
        # if self.checkBox_BananceAll.isChecked():
            # self.CheckVolBalance()
        Data = self.CheckVolBalance()
        BMU_BalanceCtrl.VolBalanceSend(self, Data)
        Data_RefreshTimer.start(1000)
        return 1
    # 均衡全选
    def BalanceChoceAll(self):
        self.checkBox_Balance_1.setCheckState(2)
        self.checkBox_Balance_2.setCheckState(2)
        self.checkBox_Balance_3.setCheckState(2)
        self.checkBox_Balance_4.setCheckState(2)
        self.checkBox_Balance_5.setCheckState(2)
        self.checkBox_Balance_6.setCheckState(2)
        self.checkBox_Balance_7.setCheckState(2)
        self.checkBox_Balance_8.setCheckState(2)
        self.checkBox_Balance_9.setCheckState(2)
        self.checkBox_Balance_10.setCheckState(2)
        self.checkBox_Balance_11.setCheckState(2)
        self.checkBox_Balance_12.setCheckState(2)
        self.checkBox_Balance_13.setCheckState(2)
        self.checkBox_Balance_14.setCheckState(2)
        self.checkBox_Balance_15.setCheckState(2)
        self.checkBox_Balance_16.setCheckState(2)
        self.checkBox_Balance_17.setCheckState(2)
        self.checkBox_Balance_18.setCheckState(2)
        self.checkBox_Balance_19.setCheckState(2)
        self.checkBox_Balance_20.setCheckState(2)
        self.checkBox_Balance_21.setCheckState(2)
        self.checkBox_Balance_22.setCheckState(2)
        self.checkBox_Balance_23.setCheckState(2)
        self.checkBox_Balance_24.setCheckState(2)

        return 1

    def BalanceChoceNone(self):
        self.checkBox_Balance_1.setCheckState(0)
        self.checkBox_Balance_2.setCheckState(0)
        self.checkBox_Balance_3.setCheckState(0)
        self.checkBox_Balance_4.setCheckState(0)
        self.checkBox_Balance_5.setCheckState(0)
        self.checkBox_Balance_6.setCheckState(0)
        self.checkBox_Balance_7.setCheckState(0)
        self.checkBox_Balance_8.setCheckState(0)
        self.checkBox_Balance_9.setCheckState(0)
        self.checkBox_Balance_10.setCheckState(0)
        self.checkBox_Balance_11.setCheckState(0)
        self.checkBox_Balance_12.setCheckState(0)
        self.checkBox_Balance_13.setCheckState(0)
        self.checkBox_Balance_14.setCheckState(0)
        self.checkBox_Balance_15.setCheckState(0)
        self.checkBox_Balance_16.setCheckState(0)
        self.checkBox_Balance_17.setCheckState(0)
        self.checkBox_Balance_18.setCheckState(0)
        self.checkBox_Balance_19.setCheckState(0)
        self.checkBox_Balance_20.setCheckState(0)
        self.checkBox_Balance_21.setCheckState(0)
        self.checkBox_Balance_22.setCheckState(0)
        self.checkBox_Balance_23.setCheckState(0)
        self.checkBox_Balance_24.setCheckState(0)
        return 1

    # 设置模块号
    def SetBMUNum(self):
        global BMU_Index
        BMU_Index = self.comboBox_BMUNum.currentIndex()



        return 1






if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
