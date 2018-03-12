#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
from robot import MyColor
import time


def run(r):
    r.drive_triple(0, 100, 70, 7, 26, 7)
    r.align_driving(70, 100, 15)
    r.drive_triple(100, 100, 0, 0, 40, 7, 0, "hold")
    r.drive_triple(0, -100, 0, 7, 40, 7, 0, "hold")



if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 1")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
