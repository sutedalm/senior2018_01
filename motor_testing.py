#!/usr/bin/env python3
from robot import Robot
import time

r = Robot()


def main():
    try:
        print("MOTOR TESTING")
        time.sleep(1)
        r._lMot.run_direct()
        r.slider.run_direct()
        speed = 100
        while not r._btn.backspace:
            if r._btn.up:
                r._lMot.duty_cycle_sp = speed
            elif r._btn.down:
                r._lMot.duty_cycle_sp = -speed
            else:
                r._lMot.duty_cycle_sp = 0

            if r._btn.right:
                r.slider.duty_cycle_sp = speed
            elif r._btn.left:
                r.slider.duty_cycle_sp = -speed
            else:
                r.slider.duty_cycle_sp = 0

    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
