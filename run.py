#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
import pt_1
import pt_2
import time


def festhalteTest(r: Robot):
        r.slider.close()
        r.drive_triple(0, 60, 0, 5, 20, 5, 0, "brake")
        r.slider.open()
        r.drive_triple(0, -60, 0, 5, 10, 5, 0, "brake")
        r.slider.close()
        r.drive_triple(0, -60, 0, 5, 10, 5, 0, "brake")


def main():
    r = Robot()
    try:
        print("running")
        # r.drive(50, 0, 50, 0, "brake", 50, 50)
        # r.drive_triple(0, 80, 0, 10, 20, 20)

        # r.drive(0, 80, 7)
        # pt_2.pick_up(r, 1)
        # r.drive(0, 90, 90, 0, "brake")
        # r.drive_triple(0, 30, 0, 30, 50, 30, 0, "brake")

        r.beep(True)
        time.sleep(2)
        # pt_1.run(r)
        # pt_2.run(r)
        # r.drive(0, 100, 47/2)
        # r.drive(100, 0, 47/2, 0, "brake")
        # r.drive(30, 0, 66, 0, "brake")
        r.drive_triple(0, 80, 0, 22, 3, 22, 0, "hold")
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
