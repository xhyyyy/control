import pygame,sys

pygame.init()
size = width,height = 600,400
speed = [1,1]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("test game")
uav = pygame.image.load("fly.jpg")
colour = 0,0,0
uavrect = uav.get_rect()
fps = 300
fclock = pygame.time.Clock()
#初始化
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type ==pygame.KEYDOWN:
            pass
    uavrect = uavrect.move(speed)
    if uavrect.left < 0 or uavrect.right > width:
        speed[0] = - speed[0]
    if uavrect.top < 0 or uavrect.bottom > height:
        speed[1]= - speed[1]
#触摸到屏幕反弹
    screen.fill(colour)
    screen.blit(uav,uavrect)
    pygame.display.update()
    fclock.tick(fps)
