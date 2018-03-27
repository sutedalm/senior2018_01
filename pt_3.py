#!/usr/bin/env python3

from robot import Robot
from robot import MyColor
import time


def next_ship(r: Robot, offset, speed_measure, speed_maximum):
    r.line_follow(speed_measure, speed_maximum, 15, offset, "run", False, False, True)
    r.line_follow(90, speed_measure, 7, offset, "run")

    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())


def run(r: Robot):
    r.ht_side.mode = 'COLOR'

    r.drive(0, 60, 5, 0, "run", 50, 50)
    r.align()
    r.drive_triple(0, 100, 0, 5, 6, 5, 0, "brake")
    r.turn(-90)

    r.drive_triple(0, 100, 0, 5, 0, 5, 0, "brake")
    r.drive(0, -80, 5, 0, "run", 50, 50)
    direction = r.get_direction_drive(-80, 0, 0, 5, "brake")
    r.turn(-direction)

    r.drive_triple(0, -80, -80, 5, 10, 5, 30)
    r.drive_triple(-80, -80, -20, 5, 5, 10, -30, "brake")

    offset = 70
    speed_measure = 30
    speed_maximum = 100

    r.line_follow(30, 70, 4, offset, "run")
    r.line_follow(70, 20, 15, offset, "brake", False, False, True)
    r.drive(0, -80, 4)
    r.drive_color(-80, -20, 15, 0, "brake", False, True)

    r.line_follow(40, speed_measure, 5, offset, "run")

    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())

    next_ship(r, offset, speed_measure, speed_maximum)

    r.line_follow(speed_measure, speed_maximum, 15, offset, "run", False, False, True)
    r.drive(speed_maximum, speed_measure, 7, 0, "run")

    print(r.ht_side.get_color().to_text())
    print(r.ht_side.value())

    next_ship(r, offset, speed_measure, speed_maximum)
    next_ship(r, offset, speed_measure, speed_maximum)

    r.drive_triple(0, -100, 0, 5, 5, 5, 0, "brake")

    r._col_l.mode = 'COL-REFLECT'
    r._col_r.mode = 'COL-REFLECT'

    r.pivot(-90)

    r.drive(0, 60, 3, 0, "run", 50, 50)
    r.align()
    r.pivot(-90, False)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 3")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
