#time:2022-10-14 order:jw
import asyncio

from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from UISource.DataTurn import DataTurn

# 系统参数设置类
from UISource.BMU_CANCOMDEAL import BMU_CANCOMDEAL


class BMU_CANPARASET(object):

    # 读取全选
    def ReadAll(tableWidget):
        row = tableWidget.rowCount()
        print('row', row)
        print('读取系统参数')
        for i in range(row):
            # 把数据写入tablewidget中
            newItem = QTableWidgetItem(str(1))
            # print(str(rowslist[j]))
            tableWidget.setItem(i+1, 2, newItem)

        return 1
    def ReadNone(tableWidget):
        row = tableWidget.rowCount()
        print('row', row)
        print('读取系统参数')
        for i in range(row):
            # 把数据写入tablewidget中
            newItem = QTableWidgetItem(str(0))
            # print(str(rowslist[j]))
            tableWidget.setItem(i+1, 2, newItem)

        return 1
    # 写入全选
    def SetAll(tableWidget):
        row = tableWidget.rowCount()
        print('row', row)
        print('设置系统参数')
        for i in range(row):
            # 把数据写入tablewidget中
            newItem = QTableWidgetItem(str(1))
            # print(str(rowslist[j]))
            tableWidget.setItem(i+1, 3, newItem)
        return 1

    def SetNone(tableWidget):
        row = tableWidget.rowCount()
        print('row', row)
        print('系统参数')
        for i in range(row):
            # 把数据写入tablewidget中
            newItem = QTableWidgetItem(str(0))
            # print(str(rowslist[j]))
            tableWidget.setItem(i+1, 3, newItem)

        return 1
    # 温度的Bx值写入
    def SetTempBx(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('温度的Bx值')
            try:
                if self.tableWidget_Para.item(10, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请先输入Bx值", QMessageBox.Yes)
                    return 0
                # 8 1
                DataTemp = []
                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(10, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0x09, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)

                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)

                if Recive_Data[0] != None:
                    self.textEdit_Para.append('Bx值下设成功\n')
                else:
                    self.textEdit_Para.append('Bx值下设成功\n')
            except:
                QMessageBox.warning(self, "提示", "请先输入Bx值", QMessageBox.Yes)
                return 0

        else:
            return 0

    # 温度的Bx值读取
    def ReadTempBx(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('温度的Bx值')

            Data = (0x00, 0x00, 0x09, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('Bx值读取\n')
            return Recive_Data
        else:
            QMessageBox.warning(self, "提示", "请先启动CAN！", QMessageBox.Yes)
            return 0

    # NTC的阻值写入
    def SetNTC(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('NTC的阻值')

            # 8 1
            DataTemp = []
            try:
                if self.tableWidget_Para.item(11, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请先输入NTC阻值", QMessageBox.Yes)
                    return 0
                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(11, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'
                print('DataVol16=', DataVol16)

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0x0A, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)
                if Recive_Data[0] != None:
                    self.textEdit_Para.append('NTC阻值下设成功\n')
                else:
                    self.textEdit_Para.append('NTC阻值下设失败\n')

            except:
                QMessageBox.warning(self, "提示", "请先输入NTC阻值", QMessageBox.Yes)
                return 0

        else:
            return 0

    # NTC的阻值读取
    def ReadNTC(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('NTC的阻值')

            Data = (0x00, 0x00, 0x0A, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('NTC阻值读取\n')
            return Recive_Data
        else:
            return 0

    # 温度总K值写入(K1)
    def SetTempK_One(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('温度总K值写入(K1)')

            # 8 1
            DataTemp = []
            # print(self.tableWidget_Para.item(6, 1).text())
            try:
                if self.tableWidget_Para.item(6, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请输入温度总K值(K1)", QMessageBox.Yes)
                    return 0
                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(6, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'
                print('DataVol16=', DataVol16)

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0xF0, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)
                if Recive_Data[0] != None:
                    self.textEdit_Para.append('K1值下设成功\n')
                    return 1
                else:
                    self.textEdit_Para.append('K1值下设失败\n')
                    return 0
            except:
                QMessageBox.warning(self, "提示", "温度总K值(K1)输入有误", QMessageBox.Yes)
                return 0

        else:
            return 0

    # 温度总K值写入(K2)
    def SetTempK_Two(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('温度总K值写入(K2)')

            # 8 1
            DataTemp = []
            try:
                if self.tableWidget_Para.item(8, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请输入温度总K值(K2)", QMessageBox.Yes)
                    return 0
                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(8, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'
                print('DataVol16=', DataVol16)

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0xF2, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)
                if Recive_Data[0] != None:
                    self.textEdit_Para.append('K2值下设成功\n')
                    return 1
                else:
                    self.textEdit_Para.append('K2值下设失败\n')
                    return 0
            except:
                QMessageBox.warning(self, "提示", "请输入温度总K值(K2)", QMessageBox.Yes)
                return 0

        else:
            return 0

    # 温度总B值写入(B1)
    def SetTempB_One(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('温度总B值写入(B1)')

            # 8 1
            DataTemp = []

            try:
                if self.tableWidget_Para.item(7, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请输入温度总B值(B1)", QMessageBox.Yes)
                    return 0
                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(7, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'
                print('DataVol16=', DataVol16)

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0xF1, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)
                if Recive_Data[0] != None:
                    self.textEdit_Para.append('B1值下设成功\n')
                    return 1
                else:
                    self.textEdit_Para.append('B1值下设失败\n')
                    return 0
            except:
                QMessageBox.warning(self, "提示", "请输入温度总B值(B1)", QMessageBox.Yes)
                return 0

        else:
            return 0

    # 温度总B值写入(B2)
    def SetTempB_Two(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('温度总B值写入(B2)')

            # 8 1
            DataTemp = []
            try:
                if self.tableWidget_Para.item(9, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请输入温度总B值(B2)", QMessageBox.Yes)
                    return 0
                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(9, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'
                print('DataVol16=', DataVol16)

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0xF3, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)
                if Recive_Data[0] != None:
                    self.textEdit_Para.append('B2值下设成功\n')
                    return 1
                else:
                    self.textEdit_Para.append('B2值下设失败\n')
                    return 0
            except:
                QMessageBox.warning(self, "提示", "请输入温度总B值(B2)", QMessageBox.Yes)
                return 0

        else:
            return 0

    # 温度总K值读取(K1)
    def ReadTempK_One(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('NTC的阻值')

            Data = (0x00, 0x00, 0xF0, 0x01, 0x00, 0x00, 0x00, 0x00)
            # print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('温度总K值读取(K1)\n')
            return Recive_Data
        else:
            return 0
    # 温度总B值读取(B1)
    def ReadTempB_One(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('NTC的阻值')

            Data = (0x00, 0x00, 0xF1, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('温度总B值读取(B1)\n')
            return Recive_Data
        else:
            return 0

    # 温度总K值读取(K2)
    def ReadTempK_Two(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('NTC的阻值')

            Data = (0x00, 0x00, 0xF2, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('温度总K值读取(K2)\n')
            return Recive_Data
        else:
            return 0

    # 温度总B值读取(B2)
    def ReadTempB_Two(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('NTC的阻值')

            Data = (0x00, 0x00, 0xF3, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('温度总B值读取(B2)\n')
            return Recive_Data
        else:
            return 0

    # DO控制合
    def DOControlOn(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180B6564
            print('DO控制')
            DataTemp = [00,00,00,00,00,00,00]
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            DataQury = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, DataQury)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            DataTemp[0] = int(('0x'+str(Recive_Data[1])[2:4]),16)
            DataTemp[1] = int(('0x' + str(Recive_Data[1])[4:6]), 16)
            DataTemp[2] = int(('0x' + str(Recive_Data[1])[6:8]), 16)
            DataTemp[3] = int(('0x' + str(Recive_Data[1])[8:10]), 16)
            DataTemp[4] = int(('0x' + str(Recive_Data[1])[10:12]), 16)
            DataTemp[5] = int(('0x' + str(Recive_Data[1])[12:14]), 16)
            DataTemp[6] = int(('0x' + str(Recive_Data[1])[14:16]), 16)

            print('DataTemp',DataTemp)

            try:
                DoOrder = self.tableWidget_Para.item(12, 1).text()
                if DoOrder == None:
                    QMessageBox.warning(self, "提示", "请输入DO序号", QMessageBox.Yes)
                    return 0
                for i in range(7):
                    print('输入值:',str(i+1))
                    if DoOrder == str(i+1):
                        DataTemp[i] = int('0x01',16)

                Data = (0x01, DataTemp[0], DataTemp[1], DataTemp[2], DataTemp[3], DataTemp[4], DataTemp[5], DataTemp[6])
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                if str(Recive_Data[0][int(DoOrder)*2:int(DoOrder)*2+2]) == '01':
                    self.textEdit_Para.append('DO合\n')
                    return 1
                else:
                    self.textEdit_Para.append('下设失败，该DO已合上或不存在\n')
                    return 0
                # print('Recive_Data=', Recive_Data)

            except:
                QMessageBox.warning(self, "提示", "请输入DO序号", QMessageBox.Yes)
                return 0

        else:
            return 0


        return Recive_Data

    # DO控制分
    def DOControlOff(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180B6564
            print('DO控制')
            try:
                DoOrder = self.tableWidget_Para.item(12, 1).text()
            except:
                QMessageBox.warning(self, "提示", "请输入DO序号", QMessageBox.Yes)
                return 0
            DataTemp = [00,00,00,00,00,00,00]
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            DataQury = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, DataQury)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            if str(Recive_Data[0][int(DoOrder) * 2:int(DoOrder) * 2 + 2]) == '00':
                self.textBrowser_Info.append('下设失败，该DO已分离或不存在\n')
                return 1
            DataTemp[0] = int(('0x'+str(Recive_Data[1])[2:4]),16)
            DataTemp[1] = int(('0x' + str(Recive_Data[1])[4:6]), 16)
            DataTemp[2] = int(('0x' + str(Recive_Data[1])[6:8]), 16)
            DataTemp[3] = int(('0x' + str(Recive_Data[1])[8:10]), 16)
            DataTemp[4] = int(('0x' + str(Recive_Data[1])[10:12]), 16)
            DataTemp[5] = int(('0x' + str(Recive_Data[1])[12:14]), 16)
            DataTemp[6] = int(('0x' + str(Recive_Data[1])[14:16]), 16)
            print('DataTemp',DataTemp)

            try:
                if self.tableWidget_Para.item(12, 1).text() == None:
                    QMessageBox.warning(self, "提示", "请输入DO序号", QMessageBox.Yes)
                    return 0
                for i in range(7):
                    print('输入值:',str(i+1))
                    if self.tableWidget_Para.item(12, 1).text() == str(i+1):
                        DataTemp[i] = int('0x00',16)

                Data = (0x01, DataTemp[0], DataTemp[1], DataTemp[2], DataTemp[3], DataTemp[4], DataTemp[5], DataTemp[6])
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                # 解析接收到的报文，如果和发送报文一致则下设成功
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                if str(Recive_Data[0][int(DoOrder)*2:int(DoOrder)*2+2]) == '00':
                    self.textEdit_Para.append('DO分\n')
                    return 1
                else:
                    self.textEdit_Para.append('DO分失败\n')
                    return 0


                # print('Recive_Data=', Recive_Data)

            except:
                QMessageBox.warning(self, "提示", "请输入DO序号", QMessageBox.Yes)
                return 0

        else:
            return 0


    # 模块地址读取
    def BMUAdress(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('模块地址')

            Data = (0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('模块地址读取\n')
            return Recive_Data
        else:
            return 0

    # 模块地址写入
    def SetBMUAdress(self):
        global BMU_Index
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('模块地址写入')

            # 8 1
            DataTemp = []
            try:

                DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(1, 1).text()).upper().lstrip("0").lstrip("X")
                # print(DataVol16)
                # print('len=',len(DataVol16))
                if len(DataTemp16) == 3:
                    DataVol16 = '0' + str(DataTemp16)
                elif len(DataTemp16) == 2:
                    DataVol16 = '00' + str(DataTemp16)
                elif len(DataTemp16) == 1:
                    DataVol16 = '000' + str(DataTemp16)
                else:
                    DataVol16 = '0000'
                print('DataVol16=', DataVol16)

                DataTemp.append(int(DataVol16[0:2], 16))
                DataTemp.append(int(DataVol16[2:4], 16))

                Data = (0x01, 0x00, 0x01, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                print('Data=', Data)
                BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                print('Recive_Data=', Recive_Data)

                if Recive_Data[0] != None:
                    self.comboBox_BMUNum.setCurrentIndex(int(self.tableWidget_Para.item(1, 1).text()))

                    self.textEdit_Para.append('模块地址更改\n')
                else:
                    self.textEdit_Para.append('模块地址更改失败\n')

            except:
                QMessageBox.warning(self, "提示", "请先输入模块地址", QMessageBox.Yes)
                return 0

        else:
            QMessageBox.warning(self, "提示", "请先打开设备!", QMessageBox.Yes)
            return 0

    # 电压个数读取
    def VolNum(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('电压个数')

            Data = (0x00, 0x00, 0x02, 0x01, 0x00, 0x18, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('电压个数读取\n')
            return Recive_Data
        else:
            return 0

    # 电压个数写入
    def SetVolNum(self):
            global BMU_Index
            if self.label_OnlineFlag.text() == '在线状态':
                BMU_ID = 0x180F6564
                print('电压个数设置')
                # 8 1
                DataTemp = []
                try:
                    DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(2, 1).text()).upper().lstrip("0").lstrip(
                        "X")
                    # print(DataVol16)
                    # print('len=',len(DataVol16))
                    if len(DataTemp16) == 3:
                        DataVol16 = '0' + str(DataTemp16)
                    elif len(DataTemp16) == 2:
                        DataVol16 = '00' + str(DataTemp16)
                    elif len(DataTemp16) == 1:
                        DataVol16 = '000' + str(DataTemp16)
                    else:
                        DataVol16 = '0000'
                    print('DataVol16=', DataVol16)

                    DataTemp.append(int(DataVol16[0:2], 16))
                    DataTemp.append(int(DataVol16[2:4], 16))

                    Data = (0x01, 0x00, 0x02, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                    # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                    print('Data=', Data)
                    BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                    BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                    Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                    print('Recive_Data=', Recive_Data)

                    if Recive_Data[0] != None:

                        self.textEdit_Para.append('电压个数设置\n')
                    else:
                        self.textEdit_Para.append('电压个数设置失败\n')

                except:
                    QMessageBox.warning(self, "提示", "请先输入电压个数", QMessageBox.Yes)
                    return 0

            else:
                QMessageBox.warning(self, "提示", "请先打开设备!", QMessageBox.Yes)
                return 0

    # 温度个数读取
    def TempNum(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('电压个数')

            Data = (0x00, 0x00, 0x08, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('电压个数读取\n')
            return Recive_Data
        else:
            return 0

    # 温度个数写入
    def SetTempNum(self):
            global BMU_Index
            if self.label_OnlineFlag.text() == '在线状态':
                BMU_ID = 0x180F6564
                print('温度个数设置')
                # 8 1
                DataTemp = []
                try:
                    DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(3, 1).text()).upper().lstrip("0").lstrip(
                        "X")
                    # print(DataVol16)
                    # print('len=',len(DataVol16))
                    if len(DataTemp16) == 3:
                        DataVol16 = '0' + str(DataTemp16)
                    elif len(DataTemp16) == 2:
                        DataVol16 = '00' + str(DataTemp16)
                    elif len(DataTemp16) == 1:
                        DataVol16 = '000' + str(DataTemp16)
                    else:
                        DataVol16 = '0000'
                    print('DataVol16=', DataVol16)

                    DataTemp.append(int(DataVol16[0:2], 16))
                    DataTemp.append(int(DataVol16[2:4], 16))

                    Data = (0x01, 0x00, 0x08, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                    # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                    print('Data=', Data)
                    BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                    BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                    Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                    print('Recive_Data=', Recive_Data)

                    if Recive_Data[0] != None:

                        self.textEdit_Para.append('温度个数设置\n')
                    else:
                        self.textEdit_Para.append('温度个数写入失败\n')

                except:
                    QMessageBox.warning(self, "提示", "请先输入温度个数", QMessageBox.Yes)
                    return 0

            else:
                QMessageBox.warning(self, "提示", "请先打开设备!", QMessageBox.Yes)
                return 0

    # 电压K值
    def VolKNum(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('电压K值')

            Data = (0x00, 0x00, 0x64, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('电压K值读取\n')
            return Recive_Data
        else:
            return 0

    # 电压K值写入
    def SetVolKNum(self):
            global BMU_Index
            if self.label_OnlineFlag.text() == '在线状态':
                BMU_ID = 0x180F6564
                print('电压K值设置')
                # 8 1
                DataTemp = []
                try:
                    DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(4, 1).text()).upper().lstrip("0").lstrip(
                        "X")
                    # print(DataVol16)
                    # print('len=',len(DataVol16))
                    if len(DataTemp16) == 3:
                        DataVol16 = '0' + str(DataTemp16)
                    elif len(DataTemp16) == 2:
                        DataVol16 = '00' + str(DataTemp16)
                    elif len(DataTemp16) == 1:
                        DataVol16 = '000' + str(DataTemp16)
                    else:
                        DataVol16 = '0000'
                    print('DataVol16=', DataVol16)

                    DataTemp.append(int(DataVol16[0:2], 16))
                    DataTemp.append(int(DataVol16[2:4], 16))

                    Data = (0x01, 0x00, 0x64, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                    # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                    print('Data=', Data)
                    BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                    BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                    Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                    print('Recive_Data=', Recive_Data)

                    if Recive_Data[0] != None:

                        self.textEdit_Para.append('电压K值设置\n')
                    else:
                        self.textEdit_Para.append('电压K值写入失败\n')

                except:
                    QMessageBox.warning(self, "提示", "请先输入电压K值", QMessageBox.Yes)
                    return 0

            else:
                QMessageBox.warning(self, "提示", "请先打开设备!", QMessageBox.Yes)
                return 0

    # 电压B值读取
    def TempBNum(self):
        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180F6564
            print('电压B值')

            Data = (0x00, 0x00, 0x65, 0x01, 0x00, 0x00, 0x00, 0x00)
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            self.textEdit_Para.append('电压B值读取\n')
            return Recive_Data
        else:
            return 0

    # 电压B值写入
    def SetTempBNum(self):
            global BMU_Index
            if self.label_OnlineFlag.text() == '在线状态':
                BMU_ID = 0x180F6564
                print('电压B值设置')
                # 8 1
                DataTemp = []
                try:
                    DataTemp16 = DataTurn.DecToHex(self.tableWidget_Para.item(5, 1).text()).upper().lstrip("0").lstrip(
                        "X")
                    # print(DataVol16)
                    # print('len=',len(DataVol16))
                    if len(DataTemp16) == 3:
                        DataVol16 = '0' + str(DataTemp16)
                    elif len(DataTemp16) == 2:
                        DataVol16 = '00' + str(DataTemp16)
                    elif len(DataTemp16) == 1:
                        DataVol16 = '000' + str(DataTemp16)
                    else:
                        DataVol16 = '0000'
                    print('DataVol16=', DataVol16)

                    DataTemp.append(int(DataVol16[0:2], 16))
                    DataTemp.append(int(DataVol16[2:4], 16))

                    Data = (0x01, 0x00, 0x65, 0x01, DataTemp[0], DataTemp[1], 0x00, 0x00)
                    # Data = (0x01, 0x00, 0x09, 0x01, 0x0D, 0x6B, 0x00, 0x00)
                    print('Data=', Data)
                    BMU_CANCOMDEAL.CAN_ClearBuffer(self)
                    BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
                    Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
                    print('Recive_Data=', Recive_Data)

                    if Recive_Data[0] != None:

                        self.textEdit_Para.append('电压B值设置\n')
                    else:
                        self.textEdit_Para.append('电压B值写入失败\n')

                except:
                    QMessageBox.warning(self, "提示", "请先输入电压B值", QMessageBox.Yes)
                    return 0

            else:
                QMessageBox.warning(self, "提示", "请先打开设备!", QMessageBox.Yes)
                return 0


