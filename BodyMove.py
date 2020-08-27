#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "H.YL"

import sys, time, os
import threading

sys.path.append(".")
from library.pyFirmata.pyfirmata import Arduino

mars = Arduino('/dev/ttyUSB0')
mutex = threading.Lock()

# ————————————————————————————————————————————————————————————————————
# ————           This class are all the basic actions             ————
# ————————————————————————————————————————————————————————————————————
class BodyMove(object):

    def __init__(self):
        """
        init the parameters
        """

        # Define the range of head degree list
        self.angList = [2 * i for i in range(1, 21)]
        self.size = len(self.angList)
        self.curInd = 19
        a = self.angList[self.curInd]

        #Get the last Voltage
        mutex.acquire()
        self.lastVoltage = mars.getBattery(0)
        time.sleep(1)
        mutex.release()


    def headUpOneStep(self):
        if self.curInd < self.size - 1:
            self.curInd += 1
            mars.setHeadAngle(1, self.angList[self.curInd], 0.8)
        else:
            pass
        # print("have been to max")

    def haedDownOneStep(self):
        if 0 < self.curInd:
            self.curInd -= 1
            mars.setHeadAngle(1, self.angList[self.curInd], 0.8)
        else:
            pass
        # print("have been to min")

    def turnLeftOneStep(self, step=12, speed=1):
        if step <= 3:
            step = 3
        if step >= 15:
            step = 15
            
        print("turn left one step")

        mutex.acquire()
        mars.setTurn(-step, speed)
        time.sleep(0.5)
        mutex.release()
        
        self.headInit()
        

    def turnRightOneStep(self, step=12, speed=1):
        if step <= 3:
            step = 3
        if step >= 15:
            step = 15
            
        print("turn right one step")

        mutex.acquire()
        mars.setTurn(step, speed)
        time.sleep(0.5)
        mutex.release()
        
        self.headInit()


    def goOneStep(self, step=0.04, delay=2):
        print("go one step")
        mutex.acquire()
        mars.setTrot(1, step, 0, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(2, step, 0, 1)
        time.sleep(delay)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(0, step, 0, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        self.headInit()
        

    def backOneStep(self, step=0.04, delay=2):
        print("back one step")
        mutex.acquire()
        mars.setTrot(1, -step, 0, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(2, -step, 0, 1)
        time.sleep(delay)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(0, -step, 0, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        self.headInit()
        

    def leftMoveOneStep(self, step=0.04, delay=2):
        print("left move one step")
        mutex.acquire()
        mars.setTrot(1, 0, step, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(2, 0, step, 1)
        time.sleep(delay)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(0, 0, step, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        self.headInit()
        

    def rightMoveOneStep(self, step=0.04, delay=2):
        print("right move one step")
        mutex.acquire()
        mars.setTrot(1, 0, -step, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(2, 0, -step, 1)
        time.sleep(delay)
        mutex.release()
        mars.setStop()
        
        mutex.acquire()
        mars.setTrot(0, 0, -step, 1)
        time.sleep(0.8)
        mutex.release()
        mars.setStop()
        
        self.headInit()
        
        
    def getTof(self):
        mutex.acquire()
        a = mars.getTof()
        time.sleep(0.1)
        mutex.release()
        return a

    def headInit(self):
        mars.setHeadAngle(1, 25, 0.8)
        mars.setHeadAngle(2, 4, 0.8)
        time.sleep(0.2)

    def staticPose(self):
        mars.setHeadAngle(1, 25, 1)
        mars.setHeadAngle(2, 4, 1)

        mars.setLegAngle(1, 1, 15, 0.8)
        mars.setLegAngle(1, 2, -18, 0.8)
        mars.setLegAngle(1, 3, 30, 0.8)

        mars.setLegAngle(2, 1, 15, 0.8)
        mars.setLegAngle(2, 2, -18, 0.8)
        mars.setLegAngle(2, 3, 30, 0.8)

        mars.setLegAngle(3, 1, 8, 0.8)
        mars.setLegAngle(3, 2, 0, 0.8)
        mars.setLegAngle(3, 3, -75, 0.8)

        mars.setLegAngle(4, 1, 8, 0.8)
        mars.setLegAngle(4, 2, 0, 0.8)
        mars.setLegAngle(4, 3, -75, 0.8)

    def ready(self, speed=0.1):
        # buttocks down
        time.sleep(1)
        mars.setLegAngle(3, 3, -100, speed)
        mars.setLegAngle(4, 3, -100, speed)
        time.sleep(0.1)

        # take a step forward
        mars.setLegAngle(3, 3, -100, speed * 0.5)
        mars.setLegAngle(3, 2, 20, speed * 0.5)
        time.sleep(1)
        mars.setLegAngle(2, 3, 60, speed * 2)
        time.sleep(0.1)
        mars.setLegAngle(2, 2, -25, speed)
        time.sleep(0.1)
        mars.setLegAngle(2, 2, 27, speed)
        time.sleep(0.1)
        mars.setLegAngle(2, 3, 0, speed)
        mars.setLegAngle(1, 3, 60, speed)
        mars.setLegAngle(3, 3, -100, speed * 0.5)
        mars.setLegAngle(3, 2, 15, speed * 0.5)
        time.sleep(0.1)

        mars.setLegAngle(1, 3, 75, speed * 2)
        time.sleep(0.1)
        mars.setLegAngle(1, 2, -25, speed)
        time.sleep(0.1)
        mars.setLegAngle(1, 2, 27, speed)
        time.sleep(0.1)
        mars.setLegAngle(1, 3, 0, speed)
        time.sleep(0.1)
        # buttocks down
        time.sleep(1)
        mars.setLegAngle(3, 3, -100, speed)
        mars.setLegAngle(4, 3, -100, speed)
        time.sleep(2)
        mars.setLegAngle(4, 2, 15, speed * 0.5)

        # buttocks up
        mars.setLegAngle(3, 3, 0, speed)
        mars.setLegAngle(4, 3, 0, speed)
        time.sleep(1)

    def stretching(self, speed=0.1):
        # buttocks up
        mars.setLegAngle(3, 3, 0, speed)
        mars.setLegAngle(4, 3, 0, speed)
        time.sleep(1)
        # hold on
        mars.setLegAngle(2, 3, 30, speed)
        time.sleep(0.5)
        mars.setLegAngle(2, 3, 0, speed)
        time.sleep(1)
        mars.setLegAngle(1, 3, 30, speed)
        time.sleep(0.5)
        mars.setLegAngle(1, 3, 0, speed)
        time.sleep(2)
        # body forward
        mars.setLegAngle(3, 3, 0, speed)
        mars.setLegAngle(4, 3, 0, speed)
        mars.setLegAngle(1, 3, 60, speed)
        mars.setLegAngle(2, 3, 60, speed)
        time.sleep(2)
        # buttocks down
        mars.setLegAngle(3, 3, -100, speed)
        mars.setLegAngle(4, 3, -100, speed)
        time.sleep(1)

    def ready2(self, speed=0.1):
        # take a step forward
        mars.setLegAngle(3, 3, -80, speed * 0.5)
        mars.setLegAngle(3, 2, 20, speed * 0.5)
        time.sleep(1)
        mars.setLegAngle(2, 3, 60, speed * 2)
        time.sleep(0.1)
        mars.setLegAngle(2, 2, -20, speed)
        time.sleep(0.1)
        mars.setLegAngle(2, 2, 25, speed)
        time.sleep(0.1)
        mars.setLegAngle(2, 3, 0, speed)
        mars.setLegAngle(1, 3, 60, speed)
        mars.setLegAngle(3, 3, -60, speed * 0.5)
        mars.setLegAngle(3, 2, 15, speed * 0.5)
        time.sleep(1)
        mars.setLegAngle(1, 3, 75, speed * 2)
        time.sleep(0.1)
        mars.setLegAngle(1, 2, -20, speed)
        time.sleep(0.1)
        mars.setLegAngle(1, 2, 25, speed)
        time.sleep(0.1)
        mars.setLegAngle(1, 3, 0, speed)
        time.sleep(0.1)
        # buttocks down
        time.sleep(1)
        mars.setLegAngle(3, 3, -100, speed)
        mars.setLegAngle(4, 3, -100, speed)
        time.sleep(1)

        time.sleep(1)
        mars.setLegAngle(1, 2, 20, 0.1)
        mars.setLegAngle(2, 2, 20, 0.1)

    def sitDown(self):
        mars.setLegAngle(1, 2, 32, 0.1)
        mars.setLegAngle(2, 2, 32, 0.1)
        mars.setLegAngle(3, 3, -40, 0.1)
        mars.setLegAngle(4, 3, -40, 0.1)

        mars.setLegAngle(1, 1, 20, 0.1)
        mars.setLegAngle(2, 1, 20, 0.1)
        time.sleep(2)
        mars.setCOGOffset(0.05, 0, -0.05, 0.1)
        time.sleep(1)

        mars.setCOGOffset(0.01, 0, -0.01, 0.1)
        time.sleep(1)
        '''
        mars.setCOGOffset(0.01, 0, -0.01, 0.1)
        time.sleep(1)
        mars.setCOGOffset(0.01, 0, -0.01, 0.1)
        time.sleep(1)
        mars.setCOGOffset(0.01, 0, -0.01, 0.1)
        time.sleep(1)
        '''

        time.sleep(2.5)
        mars.setCOGOffset(0.05, 0, 0, 0.1)
        time.sleep(2.5)
        mars.setCOGOffset(0, 0, -0.05, 0.1)
        time.sleep(2.5)

        mars.setLegAngle(1, 1, 20, 0.1)
        time.sleep(0.5)
        mars.setLegAngle(2, 1, 20, 0.1)
        time.sleep(1)
        mars.setLegAngle(1, 2, 20, 0.1)
        mars.setLegAngle(2, 2, 20, 0.1)

        time.sleep(2)
        mars.setLegAngle(3, 3, -15, 0.05)
        mars.setLegAngle(4, 3, -15, 0.05)

    def chargeCharging(slef):
        """
        Test whether charging
        :return: [bool] True or False
        """
        return mars.getBattery(0) > slef.lastVoltage


def test():
    move = BodyMove()
    time.sleep(1)
    move.staticPose()
    time.sleep(0.5)
    #time.sleep(2)
    #move.ready2()
    #time.sleep(1)
    #move.ready2()
    #time.sleep(1)
    move.goOneStep(step=0.04, delay=2)
    # move.sitDown()
    # time.sleep(3)
    # move.chargCharging()


if __name__ == "__main__":
    test()
