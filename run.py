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
        r.drive(60, 300, -60)
        r.drive(60, 300, 60)
        r.drive(60, 300)
        r.drive(-50, 300, -60)
        r.drive(-60, 300, 60)
        r.drive(-60, 300)

        r._lMot.stop(stop_action="hold")
        r._rMot.stop(stop_action="hold")
        time.sleep(0.5)
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
