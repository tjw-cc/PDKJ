Hex_Dict_Own = {
    '0':0,
    '1':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    'A':10,
    'B':11,
    'C':12,
    'D':13,
    'E':14,
    'F':15
}
# 进制转换
class DataTurn(object):
    def __init__(self, parent=None):
        super(DataTurn, self).__init__(parent)

    def crc16(x):
        Crc_Reg = 0xFFFF
        temp = 0 & 0xFFFF
        # reply = QMessageBox.information(self,"错误信息",str(x),QMessageBox.Yes | QMessageBox.No)
        # return
        while x != '':
            Data = x[:2]
            x = x[2:].strip()
            # print('x=',x)
            byte = DataTurn.HexToDec(Data)
            Crc_Reg ^= byte
            for i in range(8):
                if Crc_Reg & 0x0001 == 1:
                    Crc_Reg >>= 1
                    Crc_Reg ^= 0xA001  # 0xA001是0x8005循环右移16位的值
                else:
                    Crc_Reg >>= 1

        return hex(Crc_Reg)

    def HexToDec(x):
        num = 0
        x = str(x)
        # MainWindows.Data_Show.append(str(len(x)))
        for i in range(len(x)):
            str2 = x[i]
            str2 = str2.upper()
            #     MainWindows.Data_Show.append(str(str2))
            num += Hex_Dict_Own[str2] * pow(16, (len(x) - i - 1))
            # MainWindows.Data_Show.append(str(str2))
        return num


    # 十进制转换为16进制
    def DecToHex(x):
        x = str(x)
        result = str(hex(eval(x)))

        return result

    # 把二进制数按4位分割
    def sep_four(n):
        tlist = []
        for i in range(0, len(n) // 4):
            a = int(n[4 * i:4 * i + 4], 2)
            tlist.append("{:x}".format(a))  # 转成16进制，并添加到列表中
        return tlist
    # 二进制取反
    def reverse_func(str):
        str = str.replace('0', '2')
        str = str.replace('1', '0')
        str = str.replace('2', '1')
        return str
