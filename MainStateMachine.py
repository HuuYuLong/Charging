#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "H.YL"

import sys, time

sys.path.append(".")

from charging.ChargingStrategy import ChargingStrategy
from charging import State
from charging import LongStrategeState
from charging import MidStrategeState
from charging import ShortStrategeState


# ——————————————————————————————
# ———— Long Stratege States ————
# ——————————————————————————————
# 检测 当前是 什么状态:
class longTestState(LongStrategeState):
    def __init__(self):
        self.name = "TestState"

    def exec(self):
        print("Now long distanc, Test which state")
        print("--------------------")

        self.returndata = self.obj.longGetObstacleTargetData()

    def exit(self):
        if self.returndata == "00":
            return 1
        if self.returndata == "01":
            return 3
        if self.returndata == "10":
            return 2
        if self.returndata == "11":
            return 4
        if self.returndata == "q":
            return 5


# 定义 1: 未丢失目标 无障碍 状态，继承State
class NLostT_NObstacle(LongStrategeState):
    def __init__(self):
        self.name = "NLostT_NObstacle"

    def exec(self):
        print("Now Not lost target, not have obstacle")
        print("Now need walk to center")
        print("--------------------")

        self.obj.walk2Center()


    def exit(self):
        return 0


# 定义 2: 丢失目标 无障碍 状态
class LostT_NObstacle(LongStrategeState):
    def __init__(self):
        self.name = "LostT_NObstacle"

    def exec(self):
        print("Now lost target, not have obstacle")
        print("Now need find Target in situ")
        # print("--------------------" + str(self.obj.move))
        a = self.obj.findTargetInSitu()
        if a == None:
            print("now need wandering.")
            self.obj.wandering()

    def exit(self):
        return 0


# 定义 3: 未丢失目标 有障碍 状态
class NLostT_Obstacle(LongStrategeState):
    def __init__(self):
        self.name = "NLostT_Obstacle"

    def exec(self):
        print("Now not loss target, have obstacle")
        print("Now need to obstacle avoidance walk")
        print("--------------------")
        self.obj.obstacleAvoidanceWalk()

    def exit(self):
        return 0


# 定义 4: 丢失目标 有障碍 状态
class LostT_Obstacle(LongStrategeState):
    def __init__(self):
        self.name = "LostT_Obstacle"

    def exec(self):
        print("Now lost target, have obstcle")
        print("Now need to walk away obstacle")
        print("--------------------")
        self.obj.walkAwayObstacle()

    def exit(self):
        return 0


# 定义 5: 完成结束 状态
class Finished(State):
    def __init__(self):
        self.name = "Finished"

    def exec(self):
        print("I have been Finished")
        print("--------------------")

    def exit(self):
        return None


# ————————————————————————————————
# ———— Middle Stratege States ————
# ————————————————————————————————
# 检测 当前是 什么状态:
class midTestState(MidStrategeState):
    def __init__(self):
        self.name = "TestState"

    def exec(self):
        print("Now mid distance, Test which state")
        print("--------------------")

        self.returndata = self.obj.midGetTargetData()

    def exit(self):
        if self.returndata == "1":
            return 1

        if self.returndata == "q":
            return 5


# 1 face to marker
class notFacetoMarker(MidStrategeState):
    def __init__(self):
        self.name = "notFacetoMarker"

    def exec(self):
        print("Now Not FacetoMarker")
        print("Now need walk to center")
        print("--------------------")
        self.obj.ajustPose()

    def exit(self):
        return 0


class StateMachine(object):

    # Define init
    def __init__(self, obj):
        State.obj = obj

        # Define long distance States
        self.longStates = {
            0: longTestState(),
            1: NLostT_NObstacle(),
            2: LostT_NObstacle(),
            3: NLostT_Obstacle(),
            4: LostT_Obstacle(),
            5: Finished(),
        }

        # Define mid distance States
        self.midStates = {
            0: midTestState(),
            1: notFacetoMarker(),
            5: Finished(),
        }

    # 自动执行 直到完成
    def AutoRun(self):
        print("-------------------")
        print("start Long distance")
        curState_num = 0
        curState = self.longStates[curState_num]
        while curState_num != 5:
            curState.exec()
            nextState_num = curState.exit()
            curState_num = nextState_num
            curState = self.longStates[curState_num]
        print("end Long distance  ")
        print("-------------------")

        time.sleep(2)
        print("-------------------")
        print("start Mid distance ")
        curState_num = 0
        curState = self.midStates[curState_num]
        while curState_num != 5:
            curState.exec()
            nextState_num = curState.exit()
            curState_num = nextState_num
            curState = self.midStates[curState_num]
        print("end Mid distance   ")
        print("-------------------")


def photoTest():
    charging = ChargingStrategy()
    AC = StateMachine(charging)

    time.sleep(1)
    for i in range(3):
        charging.move.goOneStep(step=0.04, delay=1)
        time.sleep(1.2)
        
    time.sleep(1)
    charging.move.staticPose()
    time.sleep(1)
    charging.move.sitDown()


def main():
    charging = ChargingStrategy()
    AC = StateMachine(charging)
    '''
    while 1:
        print(charging.ObstacleData)
        '''
    AC.AutoRun()

    # Next is short distance Strategy
    # TODO need to test and improve
    time.sleep(1)
    #a = charging.curPoseData[2] / 9.5
    
    charging.move.goOneStep(step=0.04, delay=1)
    time.sleep(1)
    while charging.ObstacleData > 150:
        charging.move.goOneStep(step=0.015, delay=1)
        time.sleep(1)
        
    time.sleep(3)
    charging.move.staticPose()
    time.sleep(1)
    charging.move.sitDown()


if __name__ == "__main__":
    #photoTest()
    main()
