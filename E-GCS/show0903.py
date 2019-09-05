import serial, binascii, time,struct
import threading


class Serialport:
    def __init__(self, serialPort, buand):
        self.port = serial.Serial(serialPort, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()

    def read_data(self):
        global the_datas
        while 1:
            count = self.port.inWaiting()
            if count > 0:
                data = self.port.read(count)
                the_datas = the_datas + data

def cut_frame(input):
    if len(input) == 32:
        #print(input)
        headkey,newkey,keys,ledstatus,L1Y,L1X,R1Y,R1X,tobe = struct.unpack('<8h16s',input)
        print('按键状态是{0}，灯的状态是{1}，摇杆1上下值为{2}，左右为{3}，摇杆2上下为{4}，左右是{5}'.format(keys,ledstatus,L1Y,L1X,R1Y,R1X))
        return L1Y,L1X,R1Y,R1X



serialPort = 'COM6'  # 串口
baudRate = 115200  # 波特率
the_datas = bytearray()

if __name__ == '__main__':
    the_serial = Serialport(serialPort, baudRate)
    t1 = threading.Thread(target=the_serial.read_data)
    t1.setDaemon(True)
    t1.start()
    while 1:
        data_len = len(the_datas)
        i = 0
        while (i < data_len-1):
            if (the_datas[i] == 0xaa and the_datas[i + 1] == 0x55):
                datastr = the_datas[i:i + 32]
                cut_frame(datastr)
                i = i + 32
            else:
                i = i + 1
        the_datas[0:i] = b''