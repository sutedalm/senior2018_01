#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
from robot import MyColor
import time


def set_color(r: Robot, iterator):
    color = r.ht_middle.get_color()
    print(color.to_text())
    if color is not MyColor.NOCOLOR and color is not MyColor.ERROR:
        r.container_colors[iterator] = color
        iterator -= 1
    return iterator


def run(r: Robot):
    iterator = 2
    print("PART1")

    # accelerate to first line
    r.slider.close(True, 100, 5)
    r.drive_triple(20, 100, 80, 10, 25, 5)

    # align while driving over first line
    r.align_driving(80, 100, 3, 7)

    # decelerate to first container
    r.drive_triple(100, 80, 20, 6, 2, 7, 0, "brake")

    # first container
    r.slider.open()
    r.drive_triple(20, 80, 20, 8, 3, 7, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    # second container
    r.slider.open()
    r.drive_triple(0, 30, 0, 3, 1, 2, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    # third container
    r.drive_triple(0, 50, 0, 7, 3, 6, 0, "brake")
    r.slider.open()
    r.drive_triple(0, 60, 0, 8, 3, 7, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    if iterator >= 0:
        # forth container
        r.slider.open()
        r.drive_triple(0, 30, 0, 3, 0.5, 2, 0, "brake")
        r.slider.collect()

        set_color(r, iterator)

        r.drive_triple(0, -100, -60, 21, 50, 5)
    else:
        r.drive_triple(0, -100, -60, 15, 50, 5)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 1")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
