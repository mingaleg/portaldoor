#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame
from pygame import *

WIN_WIDTH = 1366
WIN_HEIGHT = 768

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

BACKGROUND_COLOR = "#004400"

import gtk.gdk

import os
PATH = os.path.dirname(os.path.abspath(__file__))

w = gtk.gdk.get_default_root_window()
sz = w.get_size()
pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
if (pb != None):
    pb.save(os.path.join(PATH, "back.png"),"png")

class Obj(sprite.Sprite):
    def __init__(self, img, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = image.load(os.path.join(PATH, img))
        sz = self.image.get_size()
        self.rect = Rect((x, y) + sz)
        self.angle = 0

    def draw(self, screen):
        angle = self.angle
        img = transform.rotate(self.image, angle)
        self.rect = img.get_rect(center=self.rect.center)
        screen.blit(img, (self.rect.x,self.rect.y))

    def move(self, dst):
        self.rect.x += dst

    def rotate(self, angle):
        self.angle += angle


def main():
    pygame.init()
    mouse.set_visible(False)
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FULLSCREEN)
    pygame.display.set_caption("Portal door")
    bg = Obj("back.png", 0, 0)
    wall = Obj("wall.png", 0, 0)
    tmprect = (391, 89)
    leftdoor = Obj("leftdoor.png", tmprect[0]-3, tmprect[1]-3)
    leftkey = Obj("leftkey.png", tmprect[0]+210, tmprect[1]+219)
    rightkey = Obj("rightkey.png", tmprect[0]+210, tmprect[1]+219)
    rightdoor = Obj("rightdoor.png", tmprect[0]+290, tmprect[1]-3)
    timer = pygame.time.Clock()

    from time import sleep

    bg.draw(screen)
    leftdoor.draw(screen)
    rightdoor.draw(screen)
    leftkey.draw(screen)
    rightkey.draw(screen)
    wall.draw(screen)
    pygame.display.update()

    def OKPASS():
        angle = 18
        for i in range(180 // angle):
            bg.draw(screen)
            leftdoor.draw(screen)
            rightdoor.draw(screen)
            leftkey.rotate(angle)
            leftkey.draw(screen)
            rightkey.rotate(angle)
            rightkey.draw(screen)
            wall.draw(screen)
            pygame.display.update()
            timer.tick(35)

        #sleep(0.3)

        def move_doors(dist, step, sleep = 50):
            mp = 1
            if (dist < 0):
                step *= -1
                dist *= -1
                mp = -1

            def _move(step):
                bg.draw(screen)
                leftdoor.move(-step)
                leftdoor.draw(screen)
                rightdoor.move(+step)
                rightdoor.draw(screen)
                leftkey.move(+step)
                leftkey.draw(screen)
                rightkey.move(-step)
                rightkey.draw(screen)
                wall.draw(screen)
                pygame.display.update()
                timer.tick(sleep)

            globdist = 0
            for i in range(dist // abs(step)):
                _move(step)
                globdist += abs(step)

            if (dist - globdist):
                _move(mp*(dist - globdist))

        move_doors(25, 5, 100)
        move_doors(-25, 10)
        move_doors(293, 20)

        sleep(0.3)

    def FAILPASS():
        angle = 24
        for i in range(360 // angle):
            bg.draw(screen)
            leftdoor.draw(screen)
            rightdoor.draw(screen)
            leftkey.rotate(angle)
            leftkey.draw(screen)
            rightkey.rotate(angle)
            rightkey.draw(screen)
            wall.draw(screen)
            pygame.display.update()
            timer.tick(50)

    import pam
    import os

    USER = os.getlogin()

    buff = ''
    while True:
        OK = False
        FAIL = False
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    if pam.authenticate(USER, buff):
                        OK = True
                    else:
                        FAIL = True
                    buff = ''
                elif e.unicode:
                    buff += e.unicode
        timer.tick(50)

        if FAIL:
            FAILPASS()
        elif OK:
            OKPASS()
            break

if __name__ == "__main__":
    main()
