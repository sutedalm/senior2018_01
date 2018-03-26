#!/usr/bin/env python3

from robot import Robot
from robot import MyColor
import time


def run(r: Robot):
    r.line_follow(40, 40, 7, 50, "brake")

    print(r.ht_side.get_color().to_text())

    r.line_follow(40, 40, 15, 50, "run", False, False, True)
    r.line_follow(40, 40, 7, 50, "brake")

    print(r.ht_side.get_color().to_text())

    r.line_follow(40, 40, 15, 50, "run", False, False, True)
    r.drive(40, 40, 7, 0, "brake")

    print(r.ht_side.get_color().to_text())

    r.line_follow(40, 40, 15, 50, "run", False, False, True)
    r.line_follow(40, 40, 7, 50, "brake")

    print(r.ht_side.get_color().to_text())

    r.line_follow(40, 40, 15, 50, "run", False, False, True)
    r.line_follow(40, 40, 7, 50, "brake")

    print(r.ht_side.get_color().to_text())


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 3")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
