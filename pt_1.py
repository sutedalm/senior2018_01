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


def filter_colors(r: Robot):
    old_colors = r.container_colors
    print("Detected colors: " + str(old_colors))
    valid_colors = [MyColor.RED, MyColor.GREEN, MyColor.BLUE, MyColor.YELLOW]
    new_colors = []

    for c in old_colors:
        if c in new_colors or c == MyColor.ERROR:
            for new_color in valid_colors:
                if new_color not in old_colors and new_color not in new_colors:
                    new_colors.append(new_color)
                    break
        else:
            new_colors.append(c)

    r.container_colors = new_colors
    print("Filtered colors: " + str(r.container_colors))


def run(r: Robot):
    iterator = 0

    print("PART1")

    r.lifter.move_to_top_position(False)

    # accelerate to first line
    r.drive_triple(0, 100, 80, 15, 15, 5)

    # align while driving over first line
    r.slider.run_to_rel_pos(position_sp=200, speed_sp=1000, stop_action="brake")
    direction = r.get_direction_drive(80, 90, 0, 10, "run", 1)  # Calculate error

    # decelerate to first container
    r.slider.open_half_to_full(False)
    r.drive(90, 100, 25)

    # first container
    r.drive_triple(100, 50, 0, 5, 0, 4.7, 0, "brake")

    r.turn(-direction)
    r.slider.collect()

    iterator = set_color(r, iterator)

    # second container
    # r.slider.open()
    r.slider.open_to_half()
    # r.drive_triple(0, 80, 0, 4.5, 0, 4.5, 0, "brake")
    r.drive_triple(r.consts.drive_min_speed, 50, r.consts.drive_min_speed, 4.5, 0, 5, 0, "brake")
    r.slider.collect(True, 15)

    iterator = set_color(r, iterator)

    # move to third container
    r.drive_triple(0, 100, 0, 3.5, 0, 3.5, 0, "brake")

    # third container
    r.slider.open()
    # r.drive_triple(0, 100, 60, 6, 3, 5, 0)
    # r.drive(60, 50, 6, 0, "brake")

    r.drive_triple(0, 100, 50, 6, 0, 4, 0, "run")
    r.drive(50, 0, 8, 0, "brake")

    r.slider.collect(True)
    iterator = set_color(r, iterator)

    if iterator <= 2:
        # forth container
        r.drive_triple(50, 50, 0, 3.5, 0, 2, 0, "brake")
        # r.slider.open()
        r.slider.open_to_half()
        r.drive_triple(r.consts.drive_min_speed, 60, r.consts.drive_min_speed, 4, 0, 4, 0, "brake")
        r.slider.collect(True, 15)

        set_color(r, iterator)

        r.lifter.move_to_bottom_position(False)
        r.drive_triple(0, -100, -80, 21, 50, 5, 1)  #schief fahren hardcode
    else:
        r.lifter.move_to_bottom_position(False)
        r.drive_triple(0, -100, -80, 15, 50, 5, 1)

    filter_colors(r)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 1")
        rob.ht_middle.mode = 'COLOR'
        rob.beep()
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
