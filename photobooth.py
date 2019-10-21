import pygame
import os
import pygame.camera
from pygame.locals import *
import RPi.GPIO as GPIO
import time

DEVICE = '/dev/video0'
SIZE = (640, 480)
SCREENSIZE = (1920, 1080)
FILENAME = 'capture.png'
BLACK = Color(0,0,0,0)
WHITE = Color(255,255,255,255)
FOLDER = '/home/pi/'

def camstream():
    pygame.init()

    os.chdir('/home/pi')

    display = pygame.display.set_mode(SCREENSIZE, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME)
    pygame.mouse.set_visible(False)

    display.fill((WHITE))
    bienvenue = pygame.image.load(FOLDER+'bienvenue.png').convert()
    display.blit(bienvenue, (0,440))
    pygame.display.flip()

    pygame.camera.init()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    cheese = pygame.image.load(FOLDER+'cheese.png').convert()
    traitement = pygame.image.load(FOLDER+'traitement.png').convert()
    c3 = pygame.image.load(FOLDER+'3.png').convert()
    c2 = pygame.image.load(FOLDER+'2.png').convert()
    c1 = pygame.image.load(FOLDER+'1.png').convert()
    chargement = pygame.image.load(FOLDER+'recall.png').convert()

    while True:
        try:
            camera = pygame.camera.Camera(DEVICE, SIZE)
            camera.start()
        except:
            continue
        break

    screen = pygame.surface.Surface(SIZE, 0, display)

    capture = True
    recall = False
    while capture:
        screen = camera.get_image(screen)
        picture = pygame.transform.scale(screen, (1920, 1080))
        display.blit(picture, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                capture = False
            elif event.type == KEYDOWN and event.key == K_r:
                capture = False
                recall = True
            elif event.type == KEYDOWN and event.key == K_s:
                pygame.image.save(screen, FILENAME)
        input_state = GPIO.input(18)
        if input_state == False:
            for i in range(3):
                screen = camera.get_image(screen) 
                picture = pygame.transform.scale(screen, (1920, 1080))
                display.blit(picture, (0,0))
                if i == 0:
                    display.blit(c3, (0,440))
                elif i == 1:
                    display.blit(c2, (0,440))
                elif i == 2:
                    display.blit(c1, (0,440))
                pygame.display.flip()
            os.system('rm '+FOLDER+'capt0000.jpg')
            os.system('gphoto2 --capture-image-and-download &')

            display.fill((WHITE))
            display.blit(cheese, (0,440))
            pygame.display.flip()

            time.sleep(4)

            display.blit(traitement, (0,440))
            pygame.display.flip()

            timestamp = os.popen('TZ="Europe/Paris" date +%H:%M:%S').read()
            timestamp = timestamp[:-1]
            time.sleep(2)
            os.system('mv /home/pi/capt0000.jpg /home/pi/photo'+timestamp+'.jpg')
            shot = pygame.image.load('/home/pi/photo'+timestamp+'.jpg').convert()
            shot = pygame.transform.scale(shot, (1920,1080))
            display.blit(shot, (0,0))
            pygame.display.flip()
            time.sleep(10)
    while recall:
        display.fill((WHITE))
        display.blit(chargement, (0,440))
        pygame.display.flip()
        photos = os.popen('ls photo* 2> /dev/null').read()
        photolib = photos.split()
        for photo in photolib:
            temp = pygame.image.load(photo).convert()
            temp = pygame.transform.scale(temp, (1920,1080))
            display.blit(temp, (0,0))
            pygame.display.flip()
            watching = True
            while watching:
                if GPIO.input(18) == False:
                    watching = False
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_q:
                        camera.stop()
                        pygame.quit()
                        return

    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
