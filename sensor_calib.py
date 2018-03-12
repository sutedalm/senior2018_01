#!/usr/bin/env python3
from robot import Robot
import time

r = Robot()


def main():
    try:
        print("CALIB")
        time.sleep(1)
        l_min = r_min = 9999
        l_max = r_max = 0
        r._lMot.run_to_rel_pos(speed_sp=150, position_sp=2*360, stop_action="hold")
        r._rMot.run_to_rel_pos(speed_sp=150, position_sp=2*360, stop_action="hold")
        while r._rMot.is_running:  # While no button is pressed.
            l_val = r._col_l._col.value()
            r_val = r._col_r._col.value()
            l_min = min(l_min, l_val)
            l_max = max(l_max, l_val)
            r_min = min(r_min, r_val)
            r_max = max(r_max, r_val)
        print("left: (" + str(l_min) + "; " + str(l_max) + ")")
        print("right: (" + str(r_min) + "; " + str(r_max) + ")")
        r.wait_until_button()
        time.sleep(0.01)  # Wait 0.01 second

    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
