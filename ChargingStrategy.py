#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "H.YL"

from charging.ArucoPoseEstimation import ArucoPoseEstimation as APE
from charging.BodyMove import BodyMove
import threading, time, random, math


# ————————————————————————————————————————————————————————————————————
# ———— This class are all the actions of the charging strategy    ————
# ————————————————————————————————————————————————————————————————————

class ChargingStrategy(object):

    # ————————————————————————————————————————————————————————————————————
    # ———— Here are the Private methoeds and INIT，use for initialize ————
    # ————————————————————————————————————————————————————————————————————

    def __init__(self):
        """
        init the parameters
        """
        self.APE = APE()  # ArucoPoseEstimation object
        self.move = BodyMove()  # BodyMove object
        self.curPoseData = [None, None, None, None]  # Use for save current Pose Data [x, y, z, theta]
        self.curColorPileData = [None, None]  # Use for save current color Pile Data
        self.ObstacleData = None
        self.lastDetect = None  # Save the last direction of target: "left" or "right"
        self.move.headInit()  # Body init
        self.move.staticPose() 
        self._detectArucoPile()  # Start thread to detect curPoseData and colorPile
        time.sleep(1)

    def _getPoseColorPileData(self):
        """
        Thread to get current ArucoMaker data and colorPile data
        :return: None
        """
        while 1:
            self.curPoseData = self.APE.getPoseData()
            # self.curColorPileData = self.APE.getColorPileData()
            time.sleep(0.05)
            if self.curPoseData[0] != None:
                if self.curPoseData[0] < 0:
                    self.lastDetect = "left"
                elif self.curPoseData[0] > 0:
                    self.lastDetect = "right"
            #                 print(self.curPoseData)
            '''
            if self.curColorPileData[0] != None:
                if self.curColorPileData[0] < 0 :
                    self.lastDetect = "left"
                elif self.curColorPileData[0] > 0 :
                    self.lastDetect = "right"
            '''

    def _detectObstacle(self):
        """
        Thread to get current TOF distance data
        :return: None
        """
        while 1:
            self.ObstacleData = self.move.getTof()
            time.sleep(1)

    def _detectArucoPile(self):
        """
        Start CAMERA thread, getPoseColorPileData thread and detectObstacle thread
        :return: None
        """
        th1 = threading.Thread(target=self.APE.main)
        th1.start()

        th2 = threading.Thread(target=self._getPoseColorPileData)
        th2.start()

        th3 = threading.Thread(target=self._detectObstacle)
        th3.start()

    # ———————————————————————————————————————————————————————————————
    # ———— Here are the Public methods，use for different States ————
    # ———————————————————————————————————————————————————————————————

    # ———— USE FOR LONG DISTANCE ————

    def wandering(self):
        """
        Random wandering when can't find target
        :return: None
        """
        # TODO need test and improve
        print("Now wandering")
        print("--------------------")
        turnProbability = 0.28
        stopTurnProbability = 0.72
        leftTurnProbability = 0.72

        times = 30  # This Wandering has (times) operations
        i = 0
        find = False
        while i < times \
              and self.curPoseData[0] == None \
              and self.ObstacleData >= 250 :  # If have detect change end loop
            
            r = random.random()

            time.sleep(1)
            self.move.goOneStep()
            
            i += 1
            if r <= turnProbability:  # Turn switch
                stop = random.random()

                time.sleep(1)
                while stop >= stopTurnProbability \
                      and self.curPoseData[0] == None \
                      and self.ObstacleData >= 250:
                    
                    stop = random.random()
                    s = random.random()
                    if s < leftTurnProbability:  # left or right
                        self.move.turnLeftOneStep()
                        i += 1
                        time.sleep(1)
                    else:
                        self.move.turnRightOneStep()
                        i += 1
                        time.sleep(1)
                    
                time.sleep(0.4)
                
        if self.ObstacleData < 250:
            self.move.backOneStep()
            time.sleep(1)
            self.move.backOneStep()
            time.sleep(1)
            self.move.backOneStep()
            time.sleep(1)
            
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
            
            self.move.goOneStep()
            time.sleep(1)
            self.move.goOneStep()
            time.sleep(1)
            self.move.goOneStep()
            time.sleep(1)   
                  
                        

    def walkAwayObstacle(self):
        """
        Getting out of the obstacles when face obstcles
        :return: None
        """
        print("Getting out of the obstacles")
        print("--------------------")

        if self.lastDetect != None:
            # while self.ObstacleData < 200:
            if self.lastDetect == "left":
                self.move.rightMoveOneStep()
                time.sleep(1)
                self.move.rightMoveOneStep()
                time.sleep(1)
                self.move.rightMoveOneStep()
                time.sleep(1)

            elif self.lastDetect == "right":
                self.move.leftMoveOneStep()
                time.sleep(1)
                self.move.leftMoveOneStep()
                time.sleep(1)
                self.move.leftMoveOneStep()
                time.sleep(1)

        else:
            self.move.leftMoveOneStep()
            time.sleep(1)
            self.move.leftMoveOneStep()
            time.sleep(1)
            self.move.leftMoveOneStep()
            time.sleep(1)
            
        
    def obstacleAvoidanceWalk(self):
        """
        Walking with avoid obstacle when get target and face obstacle
        :return: None
        """
        # TODO need test and improve
        print("Walking with avoid obstacle")
        print("--------------------")
        self.walkAwayObstacle()
        self.findTargetInSitu()
        self.walk2Center()
        

    def findTargetInSitu(self):
        """
        Finding target in situ when lost target
        :return: None
        """
        print("Finding target in situ")
        print("--------------------")
        angel = 0
        if self.curPoseData[0] != None:
            alpha = math.degrees( math.atan(self.curPoseData[0]/self.curPoseData[2]))
            theta = alpha + self.curPoseData[3]
            step = theta*0.6
        else:
            step = 10
            
        while abs(angel) < 180 and self.ObstacleData > 250:

            time.sleep(1)
            if (self.curColorPileData[0] != None):
                print(1)
                return self.curColorPileData[0]
            
            time.sleep(1)
            if (self.curPoseData[0] != None):
                print(2)
                return self.curPoseData[0]

            if self.lastDetect == "left":
                self.move.turnLeftOneStep(step = step)
                print(3)
                time.sleep(1)
                angel += step
                continue

            elif self.lastDetect == "right":
                self.move.turnRightOneStep(step = step)
                time.sleep(1)
                print(4)
                angel -= step
                continue

            # print("self.move = " + str(self.move))
            self.move.turnLeftOneStep(step = step)
            print(5)
            angel += step
            time.sleep(1)
        
        if self.ObstacleData <= 250:
            self.move.backOneStep()
            time.sleep(1)
            self.move.backOneStep()
            time.sleep(1)
            self.move.backOneStep()
            time.sleep(1)
            
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
            self.move.turnLeftOneStep()
            time.sleep(1)
        # print("1")
        return None

    def walk2Center(self):
        """
        Walking towards ArUco marker Center
        :return: None
        """
        print("Walking towards ArUco marker Center")
        print("--------------------")
        
        alpha = math.degrees( math.atan(self.curPoseData[0]/self.curPoseData[2]))

        
        # 1. Turn to the center first
        if self.lastDetect == "left":
            if alpha > 15:
                self.move.turnLeftOneStep(step=10)
                print("AAAAA")
                time.sleep(1)
            elif 2 < alpha <= 15:
                self.move.turnLeftOneStep(step=0.4*alpha)
                print("BBBB")
                time.sleep(1)
            
                
        elif self.lastDetect == "right":
            if alpha > 15:
                self.move.turnRightOneStep(step=10)
                print("AAAAA")
                time.sleep(1)
            elif 2 < alpha <= 15:
                self.move.turnRightOneStep(step=0.4*alpha)
                print("BBBB")
                time.sleep(1)
            
        # 2. then go one step
        if self.curPoseData[2]!= None and self.curPoseData[2] <= 100:
            a = (self.curPoseData[2] - 50)*0.8*0.001
            a = 0.01 if a <= 0.01 else a
            a = 0.04 if a >= 0.04 else a
            self.move.goOneStep(step=a)
            time.sleep(1)
        else: 
            self.move.goOneStep()

        time.sleep(0.4)
        
        
    def longGetObstacleTargetData(self):
        """
        Obtain obstacle and target data when long distance
        :return:    "q"  end long distance strategy
                    "00" NLostT_NObstacle
                    "01" NLostT_Obstacle
                    "10" LostT_NObstacle
                    "11" LostT_Obstacle
        """

        time.sleep(1)
        if self.curPoseData[2] != None:
            nowEndDistance = self.curPoseData[2]
            print("curPoseData z", nowEndDistance)
            if nowEndDistance <= 54:
                return "q"
            
        a = "0" if (self.curColorPileData[0] or self.curPoseData[0]) else "1"
        if self.ObstacleData == None:
            b = "0"
        elif 0 < self.ObstacleData < 200:
            b = "1"
        else:
            b = "0"

        return a + b

    # ———— USE FOR MIDDLE DISTANCE ————
    def ajustPose(self):
        """
        Adjusting the cat to the front of the center of the ArUco marker
        :return: None
        """
        print("Adjusting the cat to the front \r\n \
               of the center of the ArUco marker")
        print("--------------------")

        time.sleep(1)

        # prevent lost target
        if self.curPoseData[0] == None:
            if self.lastDetect == "left":
                print(3)
                self.move.turnLeftOneStep(step=4)
                time.sleep(1)

            elif self.lastDetect == "right":
                print(4)
                self.move.turnRightOneStep(step=4)
                time.sleep(1)
                
        # main adjust pose
        time.sleep(0.5)

        if self.curPoseData[3] != None:
            alpha = math.degrees( math.atan(self.curPoseData[0]/self.curPoseData[2]))
            theta = alpha + self.curPoseData[3]
            a = self.curPoseData[2]*math.sin(theta)
            
            a = 0.005 if abs(a)*0.01*0.8 <= 0.005 else abs(a)*0.01*0.8
            if a >= 0.02:
                a= 0.02     # a is move step
            
            #print(theta)
            if abs(alpha) >= 20:
                if alpha > 0:
                    print(1)
                    self.move.turnRightOneStep(step=alpha*0.4)
                    time.sleep(1)
                else:
                    print(2)
                    self.move.turnLeftOneStep(step=alpha*0.4)
                    time.sleep(1)

            elif (abs(theta) >= 10):
                if theta > 0:
                    print(3)
                    self.move.rightMoveOneStep(step = a)
                    time.sleep(1)
                else:
                    print(4)
                    self.move.leftMoveOneStep(step = a)
                    time.sleep(1)

            else:
                if alpha >= 8 :
                    print(5)
                    self.move.turnRightOneStep(step=alpha*0.5)
                    time.sleep(1)
                elif alpha <= -8 :
                    print(6)
                    self.move.turnLeftOneStep(step=alpha*0.5)
                    time.sleep(1)
                elif theta > 0 and alpha > 0:
                    print(7)
                    self.move.rightMoveOneStep(step = a)
                    time.sleep(1)
                elif theta < 0 and alpha < 0:
                    print(8)
                    self.move.leftMoveOneStep(step = a)
                    time.sleep(1)
                elif theta > 0 and alpha < 0:
                    print(9)
                    self.move.turnLeftOneStep(step=alpha*0.4)
                    time.sleep(1)
                elif theta < 0 and alpha > 0:
                    print(10)
                    self.move.turnRightOneStep(step=alpha*0.4)
                    time.sleep(1)

                '''
                self.move.headInit()
                
                if self.curPoseData[0] > 3:
                    print(22)
                    self.move.rightMoveOneStep(step=abs(a)*0.01*0.2)
                    time.sleep(1)
                elif self.curPoseData[0] < -3:
                    print(21)
                    self.move.leftMoveOneStep(step=abs(a)*0.01*0.2)
                    time.sleep(1)
                else:
                    pass
                    '''
        
    def midGetTargetData(self):
        """
        Obtain obstacle and target data when mid distance
        :return:  "q" end mid distance strategy
                  "1" Adjusting the cat to the front of the center of the ArUco marker
        """
        # TODO the thresholds need to be optimized
        th_theta = 3
        th_alpha = 3
        time.sleep(1)
        if self.curPoseData[0] == None:
            return "1"
        
        alpha = math.degrees( math.atan(self.curPoseData[0]/self.curPoseData[2]))
        theta = alpha + self.curPoseData[3]
        if abs(theta) <= th_theta and abs(theta) <= th_alpha:
            return "q"
        
        
        # prevent too close or too far away
        if self.curPoseData[2] != None:
            if self.curPoseData[2] <= 40:
                a = (50 - self.curPoseData[2])*0.2*0.01
                self.move.backOneStep(step=a)
                time.sleep(1)

            elif self.curPoseData[2] >= 58:
                a = (self.curPoseData[2] - 50)*0.2*0.01
                self.move.goOneStep(step=a)
                time.sleep(1)
                
        return "1"
