#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
from robot import MyColor
import time


def run(r):
    r.beep(True)
    time.sleep(2)

    r.drive_triple(0, 100, 60, 15, 15, 10)
    r.align_driving(60, 80, 10)

    # r.drive_triple(0, 100, 100, 7, 26, 7)
    # r.move_to_line(100)
    # r.drive(100, 100, 13)

    r.drive_triple(80, 40, 10, 9, 3, 3, 0, "hold")

    r.slider.open_half_to_full()
    r.drive_triple(0, 40, 0, 7, 3, 7, 0, "hold")
    r.slider.collect()
    # r.slider.close(True, 100, 15)

    r.slider.open_slow()
    r.drive_triple(0, 30, 0, 3, 2, 2, 0, "hold")
    r.slider.collect()
    # r.slider.close(True, 100, 15)

    r.drive_triple(0, 50, 0, 7, 3, 7, 0, "hold")
    r.slider.open()
    # r.drive_triple(0, -100, 0, 7, 40, 7, 0, "hold")


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 1")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
