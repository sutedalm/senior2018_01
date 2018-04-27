#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
import pt_1
import pt_2
import pt_3
import time


def main():
    r = Robot()
    try:
        print("running")
        r.beep(True)
        r.ht_middle.mode = 'COLOR'
        r.wait_until_button()
        r.reset()

        pt_1.run(r)

        pt_2.run(r, -80)
        pt_2.transition(r)

        pt_3.run(r, 100)
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
