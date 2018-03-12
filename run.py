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
        pt_1.run(r)
        pt_2.run(r)
        # r.drive(60, 30, r.distance_to_parallel_line(10, direction), 0, "hold")
        # r.pivot(90 - direction, True, 30)

        # r.align(1)
        # r.drive(0, 100, 50, 0, "hold")
        # r.pivot(-90)
        # r.pivot(90)
        # r.pivot(-90, False)
        # r.pivot(90, False)
        # r.drive(1, 100, 10, 0)
        # r.drive(100, 100, 18, 0)
        # r.drive(100, 0, 10, 0, "hold")
        # r.pivot(-90)
        # time.sleep(1)
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
