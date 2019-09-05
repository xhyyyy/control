import serial, binascii, time,struct
import threading
import pygame
from pygame.locals import *
from sys import exit



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
    global L1Y,L1X,R1Y,R1X
    #加锁
    lock.acquire()
    if len(input) == 32:
        headkey,newkey,keys,ledstatus,L1Y,L1X,R1Y,R1X,tobe = struct.unpack('<8h16s',input)
        #print('按键状态是{0}，灯的状态是{1}，摇杆1上下值为{2}，左右为{3}，摇杆2上下为{4}，左右是{5}'.format(keys,ledstatus,L1Y,L1X,R1Y,R1X))
    lock.release()
    #解锁



def the_game():
    background_image_filename = 'sky.png'
    mouse_image_filename = 'aos.png'
    pygame.init()
    screen = pygame.display.set_mode((800, 600), RESIZABLE, 32)
    pygame.display.set_caption("aostestv0.3")
    background = pygame.image.load(background_image_filename)
    the_role = pygame.image.load(mouse_image_filename)
    x, y = (0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # 接收到退出时间后退出程序
                exit()
        # 将背景图画上去
        screen.blit(background, (0, 0))

        if -1 < x <800:
            x = x + (L1X / 50) + (R1X /50)
        else:
            x = 0
        if -1 <y <600:
            y = y - (L1Y / 50) - (R1Y / 50 )
        else:
            y = 0
        # 将目标画上去
        screen.blit(the_role, (x, y))

        # 刷新画面
        pygame.display.update()

L1Y,L1X,R1Y,R1X = (0,0,0,0)
lock = threading.Lock()
serialPort = 'COM6'  # 串口
baudRate = 115200  # 波特率
the_datas = bytearray()

if __name__ == '__main__':
    the_serial = Serialport(serialPort, baudRate)
    t1 = threading.Thread(target=the_serial.read_data)

    t2 = threading.Thread(target=the_game)
    t1.setDaemon(True)
    t1.start()
    t2.setDaemon(True)
    t2.start()

    while 1:
        data_len = len(the_datas)
        print(L1X,L1Y,R1X,R1Y)
        i = 0
        while (i < data_len-1):
            if (the_datas[i] == 0xaa and the_datas[i + 1] == 0x55):
                datastr = the_datas[i:i + 32]
                cut_frame(datastr)
                i = i + 32
            else:
                i = i + 1
        the_datas[0:i] = b''
