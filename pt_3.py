#!/usr/bin/env python3

from robot import Robot
from robot import MyColor
import time


def run(r: Robot):
    r.ht_side.mode = 'COLOR'

    r.drive(0, 60, 5, 0, "run", 50, 50)
    direction = r.get_direction_drive(60, 0, 10, 5, "brake")
    r.turn(-90 - direction)
    r.drive_triple(0, 80, 0, 5, 0, 5, 0, "brake")
    r.drive(0, -60, 5, 0, "run", 50, 50)
    direction = r.get_direction_drive(-60, 0, 0, 5, "brake")
    r.turn(-direction)
    r.drive_triple(0, -80, 0, 5, 15, 5, 0, "brake")
    r.pivot(45, False)
    r.pivot(-45, False)

    r.drive_triple(0, 50, 0, 3.5, 0, 3, 0, "brake")
    time.sleep(0.2)
    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())

    r.drive_triple(0, 80, 0, 7, 4, 7, 0, "brake")
    time.sleep(0.2)
    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())
    r.drive_triple(0, 80, 0, 7, 4, 7, 0, "brake")
    time.sleep(0.2)
    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())
    r.drive_triple(0, 80, 0, 7, 4, 7, 0, "brake")
    time.sleep(0.2)
    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())
    r.drive_triple(0, 80, 0, 7, 4, 7, 0, "brake")
    time.sleep(0.2)
    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())

    #
    # r.drive_color(0, 80, 15, 0, "run", False, True)
    # r.drive(80, 0, 7, 0, "brake")
    # print(r.ht_side.get_color().to_text())
    # print(r.ht_side.value())
    # r.drive_color(0, 80, 15, 0, "run", False, True)
    # r.drive(80, 0, 7, 0, "brake")
    # print(r.ht_side.get_color().to_text())
    # print(r.ht_side.value())
    # r.drive_color(0, 80, 15, 0, "run", False, True)
    # r.drive(80, 0, 7, 0, "brake")
    # print(r.ht_side.get_color().to_text())
    # print(r.ht_side.value())
    # r.drive_color(0, 80, 15, 0, "run", False, True)
    # r.drive(80, 0, 7, 0, "brake")
    # print(r.ht_side.get_color().to_text())
    # print(r.ht_side.value())
    #
    # r.line_follow(40, 40, 7, 50, "brake")
    #
    # print(r.ht_side.get_color().to_text())
    #
    # r.line_follow(40, 40, 15, 50, "run", False, False, True)
    # r.line_follow(40, 40, 7, 50, "brake")
    #
    # print(r.ht_side.get_color().to_text())
    #
    # r.line_follow(40, 40, 15, 50, "run", False, False, True)
    # r.drive(40, 40, 7, 0, "brake")
    #
    # print(r.ht_side.get_color().to_text())
    #
    # r.line_follow(40, 40, 15, 50, "run", False, False, True)
    # r.line_follow(40, 40, 7, 50, "brake")
    #
    # print(r.ht_side.get_color().to_text())
    #
    # r.line_follow(40, 40, 15, 50, "run", False, False, True)
    # r.line_follow(40, 40, 7, 50, "brake")
    #
    # print(r.ht_side.get_color().to_text())


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 3")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
