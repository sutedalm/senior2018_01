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
    r.line_follow(speed_measure, speed_maximum, 10, offset, "run", False, False, True)
    r.line_follow(speed_maximum, speed_maximum, 5, offset, "run", False, False, True)
    r.line_follow(speed_maximum, speed_measure, 6.8, offset, "run")

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

    direction = r.get_direction_drive(60, 0, 10, 5, "brake")
    r.turn(-90 - direction)

    r.slider.hold_closed()

    # r.drive_triple(0, 100, 0, 5, 0, 5, 0, "brake")
    r.drive(0, -80, 5, 0, "run", 50, 50)
    direction = r.get_direction_drive(-80, 0, 0, 5, "brake")
    r.turn(-20 - direction)

    r.drive_triple(0, -80, 0, 5, 25, 5, -20, "brake")

    # Align to ship line
    offset = 50
    speed_measure = 35
    speed_maximum = 80

    r.line_follow(40, 70, 4, offset, "run")
    r.line_follow(70,  70, 15, offset, "brake", False, False, True)
    r.line_follow(70, 20, 9, offset, "brake")
    r.drive(0, -80, 13)
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
    r.drive(speed_maximum, speed_measure, 6.5, 0, "run")
    # time.sleep(5)

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
    r.drive(0, -100, 7, -25)
    r.drive(-100, -100, 2)
    r.drive(-100, 0, 7, 25, "brake")

    r.pivot(-90)
    return ships


def drop_off(r: Robot, speed_end=-80):
    r.slider.close(False, 100)
    r.drive_triple(80, 80, 0, 5, 8, 5, 0, "brake")
    # time.sleep(1)
    r.slider.open_for_ships()

    # r.drive_triple(0, -60, 0, 1, 0, 1, 0, "brake")
    r.lifter.move_down()

    r.drive_triple(0, -80, speed_end, 5, 4, 5, 0, "run")

    r.slider.close(False)


def target_position(destination):
    if destination in {3, 4, 5}:
        return True
    return False


def drop_food(r: Robot, positions):
    r.col_l.mode = 'COL-REFLECT'
    r.col_r.mode = 'COL-REFLECT'

    r.drive(0, 60, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(60, 0, 0, 4, "brake")
    r.turn(-direction)
    r.drive(0, -60, 2, 0, "run", 50, 50)
    direction = r.get_direction_drive(-60, 0, 4, 5, "brake")

    r.turn(90 - direction)

    position = True     # True = In front of line; False = behind line
    i = 0
    while i < 3:
        destination = positions[i]
        r.slider.hold_closed()
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

                    r.slider.open_for_ships(False)

                    r.drive(0, 80, 5, 0, "run", -1, 50)
                    r.drive(80, 80, 6)
                    drop_off(r)

                    r.col_r.set_inversed(True)
                    r.drive(-80, -80, 7, 0, "run", -1, 50)
                    r.col_r.set_inversed(False)
                    r.drive(-80, 0, 8, 0, "brake")
                    r.turn(-90)
                elif destination is 1:
                    direction = r.get_direction_drive(-80, -20, 19, 5, "brake")  # Calculate error

                    r.turn(90 - direction)

                    r.slider.open_for_ships(False)

                    r.drive(0, 60, 10, 0, "run", 50, 50)

                    r.align_driving(60, 80, 0, 2)
                    drop_off(r)

                    r.col_r.set_inversed(True)
                    r.col_l.set_inversed(True)
                    r.drive(-80, -60, 7, 0, "run", 50, 50)
                    direction = r.get_direction_drive(-60, 0, 2, 5, "brake")
                    r.col_r.set_inversed(False)
                    r.col_l.set_inversed(False)

                    r.turn(-90 - direction)
                    r.drive_triple(0, 80, 0, 5, 8, 5, 0, "brake")
                else:   # destination is 0
                    direction = r.get_direction_drive(-80, -20, 14.5, 5, "brake")  # Calculate error
                    r.pivot(-125 + direction, False)

                    r.drive(0, 60, 7, -40)

                    r.slider.open_for_ships(False)
                    r.drive(60, 60, 20, -20, "run", 50, 50)

                    r.drive(60, 80, 2, -20)
                    r.slider.close(False)
                    r.drive_triple(80, 80, 0, 5, 10, 5, -20, "brake")
                    r.slider.open_for_ships()

                    r.lifter.move_down()

                    r.drive_triple(0, -80, -60, 5, 0, 4, -30, "run")

                    r.slider.close(False)

                    r.col_l.set_inversed(True)
                    r.col_r.set_inversed(True)
                    direction = r.get_direction_drive(-60, 0, 14, 5, "brake")
                    r.col_l.set_inversed(False)
                    r.col_r.set_inversed(False)

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

                    r.slider.open_for_ships(False)

                    r.drive(0, 80, 5, 0, "run", 50, -1)
                    r.drive(80, 80, 6)

                    drop_off(r)

                    r.col_l.set_inversed(True)
                    r.drive(-80, -80, 7, 0, "run", 50, -1)
                    r.col_l.set_inversed(False)
                    r.drive(-80, 0, 8, 0, "brake")
                    r.turn(-90)
                elif destination is 4:
                    direction = r.get_direction_drive(80, 20, 24, 5, "brake")  # Calculate error

                    r.turn(90 - direction)

                    r.slider.open_for_ships(False)

                    r.drive(0, 60, 10, 0, "run", 50, 50)

                    r.align_driving(60, 80, 0, 2)

                    drop_off(r)

                    r.col_r.set_inversed(True)
                    r.col_l.set_inversed(True)
                    r.drive(-80, -60, 7, 0, "run", 50, 50)
                    direction = r.get_direction_drive(-60, 0, 2, 5, "brake")
                    r.col_r.set_inversed(False)
                    r.col_l.set_inversed(False)

                    r.turn(-90 - direction)

                    r.drive_triple(0, -80, 0, 5, 8, 5, 0, "brake")
                else:   # destination is 5
                    direction = r.get_direction_drive(80, 20, 37, 5, "brake")  # Calculate error

                    r.turn(70 - direction)

                    r.slider.open_for_ships(False)
                    r.drive_triple(0, 60, 60, 5, 5, 5, 25, "run", 50, 50)

                    r.drive(60, 80, 2, 25)
                    r.slider.close(False)
                    r.drive_triple(80, 80, 0, 5, 10, 5, 20, "brake")
                    r.slider.open_for_ships()

                    r.lifter.move_down()

                    r.drive_triple(0, -80, -60, 5, 0, 4, 35, "run")

                    r.slider.close(False)

                    r.col_l.set_inversed(True)
                    r.col_r.set_inversed(True)
                    direction = r.get_direction_drive(-60, 0, 2, 5, "brake")
                    r.col_l.set_inversed(False)
                    r.col_r.set_inversed(False)

                    r.turn(-90 - direction)
                    r.drive_triple(0, -80, 0, 5, 25, 5, 0, "brake")
        i += 1

    if position:
        r.drive(0, -80, 5, 0, "run", 50, 50)
        direction = r.get_direction_drive(-80, -20, 2, 5, "brake")  # Calculate error
        r.turn(-direction)

    r.drive(0, 60, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(60, 20, 0, 2, "brake")  # Calculate error
    r.turn(90 - direction)

    r.drive(0, -80, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(-80, 0, 0, 5, "brake")  # Calculate error
    r.turn(-direction)


def run(r: Robot):
    # for i in range(0, 3):
    #     r.beep(True)
    #     r.wait_until_button()
    #     r.lifter.move_up()
    #
    # r.wait_until_button()
    # r.beep()
    # time.sleep(2)

    r.lifter.move_to_top_position()

    ships = scan_ships(r)

    container = r.container_colors
    # container = [MyColor.BLUE, MyColor.GREEN, MyColor.YELLOW]

    positions = get_positions(ships, container)
    # positions = [5, 0, 4]
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
