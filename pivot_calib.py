#!/usr/bin/env python3

from robot import Robot
import time
import math

r = Robot()


def main():
    try:
        # r.align()
        r._lMot.position = r._rMot.position = 0
        r._lMot.stop(stop_action="hold")
        r._rMot.run_forever(speed_sp=150)
        while r.col_r.light_reflected() > 50:
            pass
        r._rMot.position = 0
        while r.col_r.light_reflected() <= 50:
            time.sleep(0.1)
        while r.col_r.light_reflected() > 50:
            time.sleep(0.1)
        while r.col_r.light_reflected() <= 50:
            time.sleep(0.1)
        while r.col_r.light_reflected() > 50:
            pass
        distance_right = r._util.deg_to_cm(r._rMot.position)
        r._rMot.stop(stop_action="hold")
        motor_distance = distance_right / (2 * math.pi)
        print("distance driven: " + str(distance_right))
        print("motor distance: " + str(motor_distance))
        r.wait_until_button()
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
