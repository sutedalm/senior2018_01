#!/usr/bin/env python3

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
        time.sleep(0.1)

        pt_1.run(r)

        pt_2.run(r, -80)
        pt_2.transition(r)

        pt_3.run(r, 100)
        # pt_3.z_main(r)
        pt_3.go_home_bitch(r)
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
