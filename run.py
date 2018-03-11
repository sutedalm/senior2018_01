#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
import time

r = Robot()


def main():
    try:
        print("running")
        r.drive(0, 70, 5)
        direction = r.get_direction(70)
        distance, turn = r.get_turn_correction_values(direction, 7.5 - r.midpoint_distance_from_line(direction))
        r.drive(70, 50, distance, turn, "hold")
        r.pivot(90, True, 50)
        r.drive(0, 100, 5)
        r.move_to_line(100)
        r.drive(100, 30, 5, 0, "hold")
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
