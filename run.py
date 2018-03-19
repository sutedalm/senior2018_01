#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
import pt_1
import pt_2
import time


def festhalte_test(r: Robot):
        r.slider.close()
        r.drive_triple(0, 60, 0, 5, 20, 5, 0, "brake")
        r.slider.open()
        r.drive_triple(0, -60, 0, 5, 10, 5, 0, "brake")
        r.slider.close()
        r.drive_triple(0, -60, 0, 5, 10, 5, 0, "brake")


def testing(r: Robot):
    # r.drive_triple(0, 50, 0, 10, 10, 10, 0, "brake")
    # r.drive_triple(0, 50, 0, 10, 10, 10, 0, "brake")
    # r.drive(0, 60, 5, 0, "run", 50, 50)
    # r.align_driving(60, 0, 3, 5, "brake")
    # r.drive(30, 30, 4, 0, "brake")
    #
    # r.lifter.move_up()
    # r.lifter.move_up()
    # r.lifter.move_up()
    #
    # time.sleep(1)
    #
    # r.drive(30, 30, 4, 0, "brake")
    #
    # r.lifter.move_down()
    # r.lifter.move_down()
    # r.lifter.move_down()
    # r.drive(0, 20, 5)
    # r.get_direction(20)
    # r.pivot(-90, True)
    # r.drive_triple(0, 100, 0, 10, 5, 15, 0, "brake")
    # r.pivot(90, False)
    # r.drive_triple(-20, -100, -20, 20, 5, 20, 0, "hold")
    # r.drive_triple(0, 80, 0, 10, 1, 10, 0, "brake")
    # r.pivot(90, True)
    # r.pivot(-90, False)
    # r.pivot(-90, False)
    r.lifter.move_up()
    time.sleep(2)
    r.lifter.move_up()
    time.sleep(2)
    r.lifter.move_up()
    time.sleep(2)
    r.lifter.move_down()
    time.sleep(2)
    r.lifter.move_down()
    time.sleep(2)
    r.lifter.move_down()
    time.sleep(2)


def main():
    r = Robot()
    try:
        print("running")
        r.beep(True)
        time.sleep(2)

        testing(r)
        # pt_1.run(r)
        # pt_2.run(r)
    finally:
        print("RESET")
        r.lifter.move_to_first_position()
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
