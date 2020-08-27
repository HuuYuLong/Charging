#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "H.YL"
import sys
sys.path.append(".")
from charging.BodyMove import BodyMove


def main_test():
    a = BodyMove()

    while 1:
        com = input(
            "    headup: 1    headdown: 2 \r\n \
            | leftturn: 7  ||  rightturn: 9 |\r\n \
                             \r\n \
                  -----------------         | \r\n \
                           go:8\r\n \
            |  leftmove: 4     rightmove: 6 | \r\n \
                          back:5\r\n \
                          \r\n \
            |      -----------------        | \r\n \
            |      -----------------        | \r\n "
        )

        if com == "1":
            a.headUpOneStep()
        elif com == "2":
            a.haedDownOneStep()
        elif com == "9":
            a.turnRightOneStep()
        elif com == "7":
            a.turnLeftOneStep()
        elif com == "8":
            a.goOneStep(step=0.05, delay=4)
        elif com == "5":
            a.backOneStep(step=0.04, delay=1)
        elif com == "4":
            a.leftMoveOneStep(step=0.04, delay=1)
        elif com == "6":
            a.rightMoveOneStep(step=0.04, delay=1)
        elif com == "d":
            b = a.getTof()
            print(b)
        elif com == "s":
            a.staticPose()
        else:
            print("error input")


if __name__ == "__main__":
    main_test()
