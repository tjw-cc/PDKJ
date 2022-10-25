import time
from ctypes import *

# 保留字段
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

RESERVED = 0

'''
AccCode验收码。SJA1000的帧过滤验收码。对经过屏蔽码过滤为“有关位”进行匹配，全部匹配成功后，此帧可以被接收。否则不接收。
AccMask屏蔽码。SJA1000的帧过滤屏蔽码。对接收的CAN帧ID进行过滤，对应位为0的是“有关位”，对应位为1的是“无关位”。屏蔽码推荐设置为0xFFFFFFFF，即全部接收。
Filter滤波方式，允许设置为0-3，
Timing0波特率定时器 0（BTR0）。
Timing1波特率定时器 1（BTR1）。设置值见下表。
Mode模式。=0表示正常模式（相当于正常节点），=1表示只听模式（只接收，不影响总线），=2表示自发自收模式（环回模式）。
'''
class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

# SubID 帧
# 基准电压发送帧ID
# TRANSMIT_ID =0x180F6564
TRANSMIT_ID =0x180F6564
# 基准电压接收帧ID
RECEIVE_ID = 0x188F6465
# 时间标识
TIME_STAMP = 0
# 是否使用时间标识
TIME_FLAG = 0
# 发送帧类型
TRANSMIT_SEND_TYPE = 1
# 接收帧类型
RECEIVE_SEND_TYPE = 0
# 是否是远程帧
REMOTE_FLAG = 0
# 是否是扩展帧
EXTERN_FLAG = 0
# 数据长度DLC
DATA_LEN = 8
# 用来接收的帧结构体数组的长度, 适配器中为每个通道设置了2000帧左右的接收缓存区
RECEIVE_LEN = 2500
# 接收保留字段
WAIT_TIME = 0
# 要发送的帧结构体数组的长度(发送的帧数量), 最大为1000, 建议设为1, 每次发送单帧, 以提高发送效率
TRANSMIT_LEN = 1
# 50帧的数据缓存
CANBuffer = [[0 for x in range(10)] for y in range(50)]
# 设置停止读数计时器
Data_RefreshTimer = QTimer()
# dll地址
Path = '../Source/DLL/ControlCAN.dll'
canLib = windll.LoadLibrary(Path)
'''
# 发送数据
# CAN帧结构体
# ID:         帧ID, 32位变量, 数据格式为靠右对齐
# TimeStamp:  设备接收到某一帧的时间标识, 时间标示从CAN卡上电开始计时, 计时单位为0.1ms
# TimeFlag:   是否使用时间标识, 为1时TimeStamp有效, TimeFlag和TimeStamp只在此帧为接收帧时才有意义
# SendType:   发送帧类型 0=正常发送(发送失败会自动重发, 重发时间为4秒, 4秒内没有发出则取消) 1=单次发送(只发送一次, 发送失败不会自动重发, 总线只产生一帧数据)[二次开发, 建议1, 提高发送的响应速度]
# RemoteFlag: 是否是远程帧 0=数据帧 1=远程帧(数据段空)
# ExternFlag: 是否是扩展帧 0=标准帧(11位ID) 1=扩展帧(29位ID)
# DataLen:    数据长度DLC(<=8), 即CAN帧Data有几个字节, 约束了后面Data[8]中的有效字节
# Data:       CAN帧的数据, 由于CAN规定了最大是8个字节, 所以这里预留了8个字节的空间, 受DataLen约束, 如DataLen定义为3, 即Data[0]、Data[1]、Data[2]是有效的
# Reserved:   保留字段
'''
class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte*8),
                ('Reserved', c_byte*3)]

class _RX_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte*8),
                ('Reserved', c_byte*3)]

# CAN通讯交互类
class BMU_CANCOMDEAL(object):

    # 打开CAN设备
    def CAN_Open(self):
        global CAN_OpenFlag
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber
        global CANPort_Information
        # 加载资源dll
        # canLib = windll.LoadLibrary(Path)

        CANDeviceName = self.comboBox_CANDevice.currentText()
        if CANDeviceName == 'ZLGCAN2':
            CANDeviceNameNumber = 3
        elif CANDeviceName == 'USBCAN2':
            CANDeviceNameNumber = 4
        CANDeviceIndex = self.comboBox_CANIndex.currentText()
        CANDeviceIndexNumber = int(CANDeviceIndex)
        CANDeviceChannel = self.comboBox_CANChannel.currentText()
        CANDeviceChannelNumber = int(CANDeviceChannel)
        BoundRate = self.comboBox_CANBoundRate.currentText()
        vic = _VCI_INIT_CONFIG()
        if BoundRate == '10Kbps':
            vic.Timing0 = 0x31
            vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x311C
        elif BoundRate == '50Kbps':
            vic.Timing0 = 0x09
            vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x091C
        elif BoundRate == '100Kbps':
            vic.Timing0 = 0x04
            vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x041C
        elif BoundRate == '125Kbps':
            vic.Timing0 = 0x03
            vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x031C
        elif BoundRate == '200Kbps':
            vic.Timing0 = 0x81
            vic.Timing1 = 0xFA
            CANDeviceBoundRate = 0x81FA
        elif BoundRate == '250Kbps':
            vic.Timing0 = 0x01
            vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x011C
        elif BoundRate == '500Kbps':
            vic.Timing0 = 0x00
            vic.Timing1 = 0x1C
            CANDeviceBoundRate = 0x001C
        elif BoundRate == '1000Kbps':
            vic.Timing0 = 0x09
            vic.Timing1 = 0x14
            CANDeviceBoundRate = 0x0914

        vic.AccCode = 0x80000008
        vic.AccMask = 0xffffffff
        vic.Filter = 1

        vic.Mode = 0

        ReturnData = canLib.VCI_OpenDevice(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
        if ReturnData != 1:
            reply = QMessageBox.warning(self, "提示", "打开设备失败！", QMessageBox.Yes)
        else:
            print('CAN设备打开成功')

        print('设置波特率: %d' % (canLib.VCI_SetReference(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, 0, pointer(c_int(CANDeviceBoundRate)))))
        # print('初始化: %d' % (canLib.VCI_InitCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vic))))
        ReturnData = canLib.VCI_InitCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vic))
        if ReturnData != 1:
            reply = QMessageBox.warning(self, "提示", "初始化失败！", QMessageBox.Yes)
            return -2  # returnFlag
        else:
            print('CAN初始化成功')

        # print('启动: %d' % (canLib.VCI_StartCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)))
        ReturnData = canLib.VCI_StartCAN(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
        if ReturnData != 1:
            reply = QMessageBox.warning(self, "提示", "CAN启动失败！", QMessageBox.Yes)
            return -3  # returnFlag
        else:
            print('CAN启动成功')

        return 1

    # 关闭CAN设备
    def CAN_Close(self):
        global CAN_OpenFlag
        # canLib = windll.LoadLibrary(Path)
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        ReturnData = canLib.VCI_CloseDevice(CANDeviceNameNumber, CANDeviceIndexNumber)
        print(ReturnData)
        if ReturnData != 1:
            reply = QMessageBox.warning(self, "提示", "CAN关闭失败！", QMessageBox.Yes)
            CAN_OpenFlag = 0
            return -4  # returnFlag
        else:
            CAN_OpenFlag = 1
            print('CAN关闭成功')
        return CAN_OpenFlag

    # 发送数据,
    # CAN_ID:CAN设备号,
    # CAN_ExternFlag:通道号,
    # Data:数据帧  SubID:ID帧
    def CAN_SendData(self,BMU_ID, Data):
        global BMU_Index
        try:
            # 加载ControlCAN.dll文件
            # canLib = windll.LoadLibrary(Path)

            # BMU_Index = self.comboBox_BMUNum.currentIndex()
            if self.comboBox_BMUNum.currentIndex()>1:
                # QMessageBox.warning(self, "提示", "请确认BMU模块选择是否正确！", QMessageBox.Yes)
                print('BMU_ID', hex(BMU_ID + (self.comboBox_BMUNum.currentIndex()-1) * 0x100))
                BMU_ID = BMU_ID + (self.comboBox_BMUNum.currentIndex()-1) * 0x100
                # return 0
            vco = _VCI_CAN_OBJ()
            vco.ID = BMU_ID
            vco.SendType = 0
            vco.RemoteFlag = 0
            vco.ExternFlag = 1
            vco.DataLen = 8
            vco.Data = (0, 0, 0, 0, 0, 0, 0, 0)
            # vco.Data = (0x01, 0x01, 0x2C, 0x02, 0x0C, 0xA1, 0x0C, 0x9B)
            vco.Data = Data
            print(hex(vco.ID))
            print('vco.Data=', bytearray(vco.Data).hex().upper())
            canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vco), 1)

            # print('清空缓冲区: %d' % (canLib.VCI_ClearBuffer(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)))
            # print('发送: %d' % (canLib.VCI_Transmit(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber, pointer(vco),1)))
        except:
            print('失败')
            return 0


    # 清空缓存
    def CAN_ClearBuffer(self):
        print('清空缓冲区: %d' % (canLib.VCI_ClearBuffer(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)))
        return 1

    # 使用协程接收数据
    async def CAN_ReciveData(self):
        global CANDeviceNameNumber
        global CANDeviceIndexNumber
        global CANDeviceChannelNumber

        # 加载ControlCAN.dll文件
        # canLib = windll.LoadLibrary(Path)
        Recive_Data = []


        # yield Recive_Data !=None
        vci_initconfig = _VCI_INIT_CONFIG(0x00000000, 0xFFFFFFFF, 0, 1, 0x01, 0x1C, 0)
        voc = _VCI_CAN_OBJ()
        voc.ID = RECEIVE_ID
        voc.TimeStamp = 0
        voc.SendType = 0
        voc.RemoteFlag = 0
        voc.ExternFlag = 1
        voc.DataLen = 8
        voc.Data = (0,0,0,0,0,0,0,0)
        LoopTimes = 0


        try:
            # 延时接收数据
            while 1:
                while (canLib.VCI_GetReceiveNum(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber) == 0):
                    LoopTimes = LoopTimes + 1
                    if(LoopTimes>1500):
                        break
                    continue
                # canLib.VCI_GetReceiveNum(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
                print("接收缓存数量：", canLib.VCI_GetReceiveNum(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber))
                receive_res = canLib.VCI_Receive(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber,
                                                 pointer(voc), 1, 0)
                # print("receive_res= ", receive_res)
                if receive_res > 0:
                    # Recive_Data.append(hex(voc.ID))
                    for i in range(receive_res):
                        # 解析一帧数据
                        print("帧ID ", hex(voc.ID))
                        print("时间 ", hex(voc.TimeStamp))
                        print('从缓存读取一帧数据:', bytearray(voc.Data).hex().upper())

                        Recive_Data.append(bytearray(voc.Data).hex().upper())
                Num = canLib.VCI_GetReceiveNum(CANDeviceNameNumber, CANDeviceIndexNumber, CANDeviceChannelNumber)
                if(Num==0):
                    Recive_Data.insert(0, hex(voc.ID))
                    break

            return Recive_Data

        except:
            return 0






    # 解析数据
    def analyse_msg(vci_can_obj):
        # 解析一帧数据
        print("帧ID ", hex(vci_can_obj.ID))
        if vci_can_obj.RemoteFlag == 0:
            print("数据帧 ")
        else:
            print("远程帧 ")
        if vci_can_obj.ExternFlag == 0:
            print("标准帧 ")
        else:
            print("扩展帧 ")
        if vci_can_obj.RemoteFlag == 0:
            print("数据: ")
            print("0", bytearray(vci_can_obj.Data).hex()[0:2])
            print("1", bytearray(vci_can_obj.Data).hex()[2:4])
            print("2", bytearray(vci_can_obj.Data).hex()[4:6])
            print("3", bytearray(vci_can_obj.Data).hex()[6:8])
            print("4", bytearray(vci_can_obj.Data).hex()[8:10])
            print("5", bytearray(vci_can_obj.Data).hex()[10:12])
            print("6", bytearray(vci_can_obj.Data).hex()[12:14])
            print("7", bytearray(vci_can_obj.Data).hex()[14:16])

