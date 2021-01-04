## windows have a pressure (determined by thier priority) that they exert on other touching windows. the pressure means they try to be bigger

import pygetwindow as gw
import math
#import keyboard
from win32api import GetSystemMetrics
import time

WINDOWS_DEFAULT_TITLES = ["Settings", "Settings", "Microsoft Store", "Microsoft Store", "Calculator", "Calculator", "Microsoft Edge", "Microsoft Edge", "Microsoft Edge", "Form1", "Microsoft Text Input Application", "Program Manager"]

def getMinSize(window):
    previousSize = window.size
    window.resizeTo(1, 1)
    minSize = window.size
    window.resizeTo(previousSize[0], previousSize[1])
    return minSize

def getScreenSize():
    return (GetSystemMetrics(0), GetSystemMetrics(1))

def toPressurizedWindow(win):
    win.__class__ = PressurizedWindow

def isValid(win):
    return (not (win.title in WINDOWS_DEFAULT_TITLES)) and len(win.title) > 0

def getAllWindows():
    return [win for win in gw.getAllWindows() if isValid(win)]

class PressurizedWindow(gw.Win32Window):
    _internalPressure = 10000
    def setInternalPressure(self, newPressure):
        self._internalPressure = newPressure
    def getPressure(self):
        return self._internalPressure/self.area
    def collidingWithEdge(self):
        if (#self.topleft[0] <= 0 or
          #self.topleft[1] <= 0 or
          #self.bottomright[0] >= getScreenSize()[0] or
          self.bottomright[1] >= getScreenSize()[1]):
            return True
        print(self.topleft)
        print(self.bottomright)
        return False
    def getTouching(self):
        colliding = []
        for win in getAllWindows():
            if len(win.title) > 0 and self._hWnd != win._hWnd:
                r1x = self.topleft[0]
                r1y = self.topleft[1]
                r1w = self.bottomright[0] - self.topleft[0]
                r1h = self.bottomright[1] - self.topleft[1]
                r2x = win.topleft[0]
                r2y = win.topleft[1]
                r2w = win.bottomright[0] - win.topleft[0]
                r2h = win.bottomright[1] - win.topleft[1]
                if (r1x + r1w >= r2x and     # r1 right edge past r2 left
                  r1x <= r2x + r2w and       # r1 left edge past r2 right
                  r1y + r1h >= r2y and       # r1 top edge past r2 bottom
                  r1y <= r2y + r2h):
                    colliding.append(win)
                    #print('\t%s' % str(win))
        return colliding

def moveActiveTo(direction):
    win = gw.getActiveWindow()
    toPressurizedWindow(win)
    if win != None:
        print(win.area, win.getPressure())
        print(win, win.getTouching())
        if direction == 'left':
            win.moveTo(0, win.topleft[1])
        elif direction == 'up':
            win.moveTo(win.topleft[0], 0)
        elif direction == 'down':
            win.moveTo(win.topleft[0], getScreenSize()[1] - win.size[1])
        elif direction == 'right':
            win.moveTo(getScreenSize()[0] - win.size[0], win.topleft[1])

while True:
    time.sleep(.005)
    for win in getAllWindows():
        toPressurizedWindow(win)
        if len(win.getTouching()) < 1 and not win.collidingWithEdge():
            win.move(0, win.area//10000)
            print(win.title, 'is at', win.topleft)
        print(win.title)

#DIRECTIONS = ['up', 'down', 'left', 'right']

#for direction in DIRECTIONS:
    #keyboard.add_hotkey('ctrl + alt + ' + direction, moveActiveTo, args = [direction])

#keyboard.wait('` + esc')