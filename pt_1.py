#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
from robot import MyColor
import time


def run(r: Robot):
    iterator = 2

    r.slider.close(True, 100, 5)
    r.drive_triple(0, 100, 60, 15, 15, 10)

    r.align_driving(60, 80, 3, 7)

    r.drive_triple(80, 60, 10, 6, 6, 3, 0, "brake")

    # first container
    r.slider.open()
    r.drive_triple(0, 60, 0, 8, 3, 7, 0, "brake")
    r.slider.collect()

    color = r.ht_middle.get_color()
    print(color.to_text())
    if color is not MyColor.NOCOLOR and color is not MyColor.ERROR:
        r.container_colors[iterator] = color
        iterator -= 1


    # second container
    r.slider.open()
    r.drive_triple(0, 30, 0, 3, 0.5, 2, 0, "brake")
    r.slider.collect()

    color = r.ht_middle.get_color()
    print(color.to_text())
    if color is not MyColor.NOCOLOR and color is not MyColor.ERROR:
        r.container_colors[iterator] = color
        iterator -= 1
    # r.slider.close(True, 100, 15)

    # third container
    r.drive_triple(0, 50, 0, 7, 3, 7, 0, "brake")
    r.slider.open()
    r.drive_triple(0, 60, 0, 8, 3, 7, 0, "brake")
    r.slider.collect()

    color = r.ht_middle.get_color()
    print(color.to_text())
    if color is not MyColor.NOCOLOR and color is not MyColor.ERROR:
        r.container_colors[iterator] = color
        iterator -= 1

    if iterator >= 0:
        r.slider.open()
        r.drive_triple(0, 30, 0, 3, 0.5, 2, 0, "brake")
        r.slider.collect()

        color = r.ht_middle.get_color()
        print(color.to_text())
        if color is not MyColor.NOCOLOR and color is not MyColor.ERROR:
            r.container_colors[iterator] = color
            iterator -= 1

        r.drive_triple(0, -80, -60, 21, 50, 5)
    else:
        r.drive_triple(0, -80, -60, 15, 50, 5)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 1")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
