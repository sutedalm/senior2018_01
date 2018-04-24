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
    print(color.name)
    if color is not MyColor.NOCOLOR and color is not MyColor.ERROR:
        r.container_colors[iterator] = color
        iterator += 1
    return iterator


def run(r: Robot):
    iterator = 0

    print("PART1")

    r.lifter.move_to_top_position(False)

    # accelerate to first line
    r.drive_triple(0, 100, 80, 10, 20, 5)

    # align while driving over first line
    r.slider.run_to_rel_pos(position_sp=200, speed_sp=1000, stop_action="brake")
    direction = r.get_direction_drive(80, 70, 0, 8, "run", 3)  # Calculate error

    # decelerate to first container
    r.slider.open_half_to_full(False)
    # r.drive_triple(80, 100, 100, 10, 5, 13)
    r.drive(70, 100, 28)
    # r.drive_triple(100, 80, 20, 9, 2, 4, 0)

    # first container
    r.drive_triple(100, 100, 40, 0, 3, 7, 0, "brake")
    r.turn(-direction)
    r.slider.collect()

    iterator = set_color(r, iterator)

    # second container
    r.slider.open()
    r.drive_triple(0, 80, 0, 4.5, 0, 4.5, 0, "brake")
    r.slider.collect()

    iterator = set_color(r, iterator)

    # move to third container
    r.drive_triple(0, 100, 0, 3.5, 0, 3.5, 0, "brake")

    # third container
    r.slider.open()
    r.drive_triple(0, 100, 60, 6, 3, 5, 0)
    r.drive(60, 50, 6, 0, "brake")
    r.slider.collect(True)
    iterator = set_color(r, iterator)

    if iterator <= 2:
        # forth container
        r.drive_triple(50, 50, 0, 3.5, 0, 2, 0, "brake")
        r.slider.open()
        r.drive_triple(0, 60, 0, 4, 0, 4, 0, "brake")
        r.slider.collect()

        set_color(r, iterator)

        r.lifter.move_to_first_position(False)
        r.drive_triple(0, -100, -80, 21, 50, 5)
    else:
        r.lifter.move_to_first_position(False)
        r.drive_triple(0, -100, -80, 15, 50, 5)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 1")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
