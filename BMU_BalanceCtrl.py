import asyncio



from UISource.BMU_CANCOMDEAL import BMU_CANCOMDEAL


class BMU_BalanceCtrl(object):

    def __init__(self, parent=None):
        super(BMU_BalanceCtrl, self).__init__(parent)

    # 被动均衡状态初始化
    def VolBalanceTimer(self,Data):


        return 0



    # 均衡控制
    def VolBalanceSend(self,Data):

        if self.label_OnlineFlag.text() == '在线状态':
            BMU_ID = 0x180A6564
            print('Data=', Data)
            BMU_CANCOMDEAL.CAN_ClearBuffer(self)
            BMU_CANCOMDEAL.CAN_SendData(self, BMU_ID, Data)
            Recive_Data = asyncio.run(BMU_CANCOMDEAL.CAN_ReciveData(self))
            print('Recive_Data=', Recive_Data)
            # self.textBrowser_Info.append('被动均衡下设成功\n')
            print('被动均衡')

        else:
            return 0

        return  1