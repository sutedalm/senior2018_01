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

    print("POSITIONS: " + str(positions[0]) + '; ' + str(positions[1]) + '; ' + str(positions[2]))

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
    r.slider.close(False)
    r.drive(0, 60, 5, 0, "run", 50, 50)
    r.align()
    r.drive_triple(0, 100, 0, 5, 6, 5, 0, "brake")
    r.turn(-90)

    r.slider.hold_closed()

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
    r.drive(0, -100, 7, -20)
    r.drive(-100, 0, 7, 15, "brake")

    r.pivot(-90)
    r.slider.open_for_ships()
    return ships


def drop_off(r: Robot, speed_start=0, speed_end=-80):
    r.drive(speed_start, 80, 2)
    r.slider.close(False)
    r.drive_triple(80, 80, 0, 5, 8, 5, 0, "brake")
    r.slider.open_for_ships()

    # r.drive_triple(0, -60, 0, 1, 0, 1, 0, "brake")
    r.lifter.move_down()

    r.drive_triple(0, -80, speed_end, 5, 4, 5, 0, "run")


def target_position(destination):
    if destination in {3, 4, 5}:
        return True
    return False


def drop_food(r: Robot, positions):
    r.col_l.mode = 'COL-REFLECT'
    r.col_r.mode = 'COL-REFLECT'

    r.drive(0, 60, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(60, 0, 0, 1, "brake")

    r.pivot(-90 + direction, False)

    position = True     # True = In front of line; False = behind line
    i = 0
    while i < 3:
        destination = positions[i]
        if position:
            r.drive(0, -80, 5, 0, "run", 50, 50)
            position = False

            if target_position(destination):
                direction = r.get_direction_drive(-80, -20, 2, 5, "brake")  # Calculate error
                r.turn(-direction)
                i -= 1
            else:
                if destination is 2:
                    direction = r.get_direction_drive(-80, -20, 1, 5, "brake")  # Calculate error
                    r.turn(90 - direction)
                    r.drive(0, 80, 10, 0, "run", -1, 50)

                    drop_off(r, 80)

                    r.col_r.set_inversed(True)
                    r.drive(-80, -80, 7, 0, "run", -1, 50)
                    r.col_r.set_inversed(False)
                    r.drive(-80, 0, 9, 0, "brake")
                    r.turn(-90)
                elif destination is 1:
                    direction = r.get_direction_drive(-80, -20, 19, 5, "brake")  # Calculate error
                    r.turn(90 - direction)
                    r.drive_triple(0, 80, 0, 5, 2, 3, 0, "brake", 50, 50)
                    r.align()

                    drop_off(r, 0, -60)

                    r.col_r.set_inversed(True)
                    r.col_l.set_inversed(True)
                    r.drive(-60, 0, 7, 0, "brake", 50, 50)
                    r.col_r.set_inversed(False)
                    r.col_l.set_inversed(False)
                    r.align()
                    r.drive_triple(0, -80, 0, 5, 0, 4, 0, "brake")
                    r.turn(-90)
                    r.drive_triple(0, 80, 0, 5, 8, 5, 0, "brake")
                else:   # destination is 0
                    direction = r.get_direction_drive(-80, -20, 17, 5, "brake")  # Calculate error
                    r.pivot(-115 + direction, False)

                    r.drive(0, 60, 5, -15)
                    r.drive(60, 60, 20, -15, "run", 50, 50)

                    r.drive(60, 80, 2, -15)
                    r.slider.close(False)
                    r.drive_triple(80, 80, 0, 5, 10, 5, -15, "brake")
                    r.slider.open_for_ships()

                    r.lifter.move_down()

                    r.drive_triple(0, -80, -60, 5, 0, 4, -20, "run")
                    r.col_l.set_inversed(True)
                    r.col_r.set_inversed(True)
                    direction = r.get_direction_drive(-60, 0, 14, 5, "brake")
                    r.col_l.set_inversed(False)
                    r.col_r.set_inversed(False)

                    # r.drive_triple(0, -80, 0, 5, 5, 5, 0, "brake")

                    # r.turn(-90 - direction)
                    # r.drive(-40, 0, 1, 0, "brake")
                    r.pivot(-90 - direction, True)
                    r.drive_triple(0, 80, 0, 5, 11, 5, 0, "brake")

        else:
            r.drive(0, 80, 3, 0, "run", 50, 50)
            position = True

            if not target_position(destination):
                direction = r.get_direction_drive(80, 20, 2, 5, "brake")  # Calculate error
                r.turn(-direction)
                i -= 1
            else:
                if destination is 3:
                    direction = r.get_direction_drive(80, 20, 6, 5, "brake")  # Calculate error
                    r.turn(90 - direction)
                    r.drive(0, 80, 10, 0, "run", 50, -1)

                    drop_off(r, 80)

                    r.col_l.set_inversed(True)
                    r.drive(-80, -80, 7, 0, "run", 50, -1)
                    r.col_l.set_inversed(False)
                    r.drive(-80, 0, 9, 0, "brake")
                    r.turn(-90)
                elif destination is 4:
                    direction = r.get_direction_drive(80, 20, 24, 5, "brake")  # Calculate error
                    r.turn(90 - direction)
                    r.drive_triple(0, 80, 0, 5, 2, 3, 0, "brake", 50, 50)
                    r.align()

                    drop_off(r)

                    r.col_r.set_inversed(True)
                    r.col_l.set_inversed(True)
                    r.drive(-60, 0, 7, 0, "brake", 50, 50)
                    r.col_r.set_inversed(False)
                    r.col_l.set_inversed(False)
                    r.align()
                    r.drive_triple(0, -80, 0, 5, 0, 4, 0, "brake")
                    r.turn(-90)
                    r.drive_triple(0, -80, 0, 5, 8, 5, 0, "brake")
                else:   # destination is 5
                    pass
        i += 1


def run(r: Robot):
    for i in range(0, 3):
        r.beep(True)
        r.wait_until_button()
        r.lifter.move_up()

    r.wait_until_button()
    r.beep()
    time.sleep(2)

    ships = scan_ships(r)

    container = r.container_colors
    container = [MyColor.BLUE, MyColor.GREEN, MyColor.YELLOW]

    positions = get_positions(ships, container)

    drop_food(r, positions)    # Add positions
    # drop_off(r)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 3")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
