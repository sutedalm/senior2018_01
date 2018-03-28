#!/usr/bin/env python3

from robot import Robot
from robot import MyColor
import time


def get_positions(ships, container):
    ship_flags = [False, False, False, False, False, False]
    container_flags = [False, False, False]
    positions = [0, 0, 0]

    # Color with same Color
    for container_iterator in range(0, 3):
        if container[container_iterator] is MyColor.NOCOLOR:
            container[container_iterator] = MyColor.ERROR

        if container[container_iterator] is not MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in range(0, 6):
                if ships[ship_iterator] is container[container_iterator] and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Color with Error
    for container_iterator in range(0, 3):
        if container[container_iterator] is not MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in range(0, 6):
                if ships[ship_iterator] is MyColor.ERROR and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Error with different Color or Error
    for container_iterator in range(0, 3):
        if container[container_iterator] is MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in range(0, 6):
                if ships[ship_iterator] is not MyColor.NOCOLOR and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Color with different Color (or Error)
    for container_iterator in range(0, 3):
        if container[container_iterator] is not MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in range(0, 6):
                if ships[ship_iterator] is not MyColor.NOCOLOR and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Last ship (not scanned)
    for container_iterator in range(0, 3):
        if not container_flags[container_iterator]:
            if not ship_flags[5]:
                positions[container_iterator] = 5
                ship_flags[5] = True
                container_flags[container_iterator] = True
                break

    # Rest with Nocolor
    for container_iterator in range(0, 3):
        if not container_flags[container_iterator]:
            for ship_iterator in range(0, 6):
                if not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    return positions


def next_ship(r: Robot, offset, speed_measure, speed_maximum):
    r.line_follow(speed_measure, speed_maximum, 15, offset, "run", False, False, True)
    r.line_follow(90, speed_measure, 7, offset, "run")

    color = r.ht_side.get_color()
    print(color.to_text())
    print(r.ht_side.value())
    return color


def scan_ships(r: Robot):
    r.ht_side.mode = 'COLOR'
    ships = [MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR]

    # Move to ship line
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

    # Align to ship line
    offset = 70
    speed_measure = 30
    speed_maximum = 100

    r.line_follow(30, 70, 4, offset, "run")
    r.line_follow(70, 20, 15, offset, "brake", False, False, True)
    r.drive(0, -80, 4)
    r.drive_color(-80, -20, 15, 0, "brake", False, True)

    # Start ship scanning

    # first ship
    r.line_follow(40, speed_measure, 5, offset, "run")

    color = r.ht_side.get_color()
    print(color.to_text())
    print(r.ht_side.value())
    ships[0] = color

    # second ship
    ships[1] = next_ship(r, offset, speed_measure, speed_maximum)

    # third ship
    r.line_follow(speed_measure, speed_maximum, 15, offset, "run", False, False, True)
    r.drive(speed_maximum, speed_measure, 7, 0, "run")

    color = r.ht_side.get_color()
    print(color.to_text())
    print(r.ht_side.value())
    ships[2] = color

    # forth ship
    ships[3] = next_ship(r, offset, speed_measure, speed_maximum)
    # fifth ship
    ships[4] = next_ship(r, offset, speed_measure, speed_maximum)
    ships[5] = MyColor.NOCOLOR

    # Move to center
    r.drive_triple(0, -100, 0, 5, 5, 5, 0, "brake")

    r.col_l.mode = 'COL-REFLECT'
    r.col_r.mode = 'COL-REFLECT'

    r.pivot(-90)

    r.drive(0, 60, 3, 0, "run", 50, 50)
    r.align()
    r.pivot(-90, False)


def run(r: Robot):
    scan_ships(r)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 3")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
