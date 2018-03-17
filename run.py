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
        r.beep(True)
        time.sleep(2)

        r.drive(30, 30, 4, 0, "brake")

        r.lifter.move_up()
        r.lifter.move_up()
        r.lifter.move_up()

        time.sleep(1)

        r.drive(30, 30, 4, 0, "brake")

        r.lifter.move_down()
        r.lifter.move_down()
        r.lifter.move_down()

        # r.drive(50, 0, 50, 0, "brake", 50, 50)
        # r.drive_triple(0, 80, 0, 10, 20, 20)

        # r.drive(0, 80, 7)
        # pt_2.pick_up(r, 1)
        # r.drive(0, 90, 90, 0, "brake")
        # r.drive_triple(0, 30, 0, 30, 50, 30, 0, "brake")

        # r.beep(True)
        # time.sleep(2)
        # pt_1.run(r)
        # pt_2.run(r)
        # r.pivot(-90, True)
        # r.drive_triple(0, 100, 0, 10, 5, 10, 0, "brake")
        # r.pivot(90, False)
        # r.drive_triple(-20, -100, -20, 20, 5, 20, 0, "hold")
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
