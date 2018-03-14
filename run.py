#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
import pt_1
import pt_2
import time


def main():
    r = Robot()
    try:
        print("running")
        # r.drive(0, 90, 90, 0, "hold")
        # r.drive_triple(0, 30, 0, 30, 50, 30, 0, "hold")
        # time.sleep(1)
        pt_1.run(r)
        # pt_2.run(r)
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
