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
        r.drive(0, 60, 5)
        print("running")
        direction = r.get_direction(60)
        print("direction: " + str(direction))
        distance, turn = r.get_turn_correction_values(direction, 7)
        print("distance: " + str(distance) + "; turn: " + str(turn))
        r.drive(60, 30, distance, turn, "hold")
        r.pivot(90)
        r.drive(0, 60, 5)
        r.drive(60, 30, 10, 0, "hold")
        # r.drive(30, 0, r.distance_to_parallel_line(10, direction), 0, "hold")
        # r.pivot(90 - direction)

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
