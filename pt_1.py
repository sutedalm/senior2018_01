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
        iterator += 1
    return iterator


def run(r: Robot):
    iterator = 0

    print("PART1")

    r.lifter.move_to_top_position(False)

    # accelerate to first line
    # r.slider.close(True, 100, 5)
    r.drive_triple(0, 100, 80, 5, 30, 5)

    # align while driving over first line
    # r.align_driving(80, 100, 3, 7)
    direction = r.get_direction_drive(80, 100, 0, 10, "brake")  # Calculate error

    # decelerate to first container
    r.drive_triple(100, 80, 20, 9, 2, 4, 0, "brake")

    r.turn(-direction)

    # first container
    r.slider.open_half_to_full()
    r.drive_triple(0, 100, 40, 8, 3, 7, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    # second container
    r.slider.open()
    r.drive_triple(0, 80, 0, 4, 0, 3, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    r.drive_triple(0, 100, 0, 7, 0, 6, 0, "brake")

    # third container
    r.slider.open()
    r.drive_triple(0, 100, 60, 8, 2, 3, 0)
    r.drive(60, 0, 5, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    if iterator <= 2:
        # forth container
        r.drive_triple(0, 60, 0, 8, 3, 7, 0, "brake")
        r.slider.open()
        r.drive_triple(0, 30, 0, 3, 0.5, 2, 0, "brake")
        r.slider.collect()

        set_color(r, iterator)

        r.lifter.move_to_first_position(False)
        r.drive_triple(0, -100, -60, 21, 50, 5)
    else:
        r.lifter.move_to_first_position(False)
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
