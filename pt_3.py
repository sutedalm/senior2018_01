#!/usr/bin/env python3

from robot import Robot
from robot import MyColor
import time


def get_positions(ships, container):
    ship_flags = [False, False, False, False, False, False]
    container_flags = [False, False, False]
    iteration_range = [3, 2, 4, 1, 5, 0]
    positions = [0, 0, 0]

    # Color with same Color
    for container_iterator in range(0, 3):
        if container[container_iterator] is MyColor.NOCOLOR:
            container[container_iterator] = MyColor.ERROR

        if container[container_iterator] is not MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in iteration_range:
                if ships[ship_iterator] is container[container_iterator] and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Color with Error
    for container_iterator in range(0, 3):
        if container[container_iterator] is not MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in iteration_range:
                if ships[ship_iterator] is MyColor.ERROR and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Error with different Color or Error
    for container_iterator in range(0, 3):
        if container[container_iterator] is MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in iteration_range:
                if ships[ship_iterator] is not MyColor.NOCOLOR and not ship_flags[ship_iterator]:
                    positions[container_iterator] = ship_iterator
                    ship_flags[ship_iterator] = True
                    container_flags[container_iterator] = True
                    break

    # Color with different Color (or Error)
    for container_iterator in range(0, 3):
        if container[container_iterator] is not MyColor.ERROR and not container_flags[container_iterator]:
            for ship_iterator in iteration_range:
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
            for ship_iterator in iteration_range:
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
    print(color.name)
    print(r.ht_side.value())
    return color


def drop_0(r: Robot):
    direction = r.get_direction_drive(-80, 0, 0, 5, "brake")  # Calculate error
    r.turn(-direction)
    r.drive_triple(0, -100, 0, 5, 23.5, 5, 0, "brake")

    r.turn(105)

    r.slider.position = 0
    r.slider.open_for_ships(False)
    while r.slider.position < 20:
        time.sleep(0.01)

    r.drive_triple(0, 60, 60, 5, 5, 5, -30, "run", 50, 50)

    r.drive(60, 80, 3.5, -15)
    r.slider.close(False)
    r.drive_triple(80, 80, 0, 5, 8, 5, 0, "brake")
    r.slider.open_after_ships()

    r.lifter.move_down()

    r.drive_triple(0, -80, -60, 5, 0, 4, -20, "run")

    r.slider.close(False)

    r.col_l.set_inversed(True)
    r.col_r.set_inversed(True)
    direction = r.get_direction_drive(-60, 0, 1, 5, "brake")
    r.col_l.set_inversed(False)
    r.col_r.set_inversed(False)

    r.turn(-90 - direction)
    r.drive_triple(0, 100, 80, 5, 17, 5, 0, "run", 50, 50)
    # r.drive_triple(0, 80, 0, 5, 20, 5, 0, "brake")


def drop_1(r: Robot):
    direction = r.get_direction_drive(-80, -100, 0, 5)  # Calculate error
    r.drive_triple(-100, -100, 0, 0, 14, 5, 0, "brake")

    r.turn(90 - direction)

    r.slider.position = 0
    r.slider.open_for_ships(False)
    while r.slider.position < 20:
        time.sleep(0.01)
    # r.slider.wait_while('running')

    r.drive(0, 60, 10, 0, "run", 50, 50)

    r.align_driving(60, 80, 0, 2.5)
    drop_off(r)

    r.col_r.set_inversed(True)
    r.col_l.set_inversed(True)
    r.drive(-80, -60, 7, 0, "run", 50, 50)
    direction = r.get_direction_drive(-60, 0, 1.5, 5, "brake")
    r.col_r.set_inversed(False)
    r.col_l.set_inversed(False)

    r.turn(-90 - direction)
    r.drive_triple(0, 100, 80, 5, 10, 3, 0, "run", 50, 50)
    # r.drive_triple(0, 80, 0, 5, 8, 5, 0, "brake")


def drop_2(r: Robot):
    direction = r.get_direction_drive(-80, -20, 1, 5, "brake")  # Calculate error

    r.turn(90 - direction)

    r.slider.position = 0
    r.slider.open_for_ships(False)
    while r.slider.position < 20:
        time.sleep(0.01)

    r.drive(0, 80, 5, 0, "run", -1, 50)
    r.drive(80, 80, 6.5)
    drop_off(r)

    r.col_r.set_inversed(True)
    r.drive(-80, -80, 6.5, 0, "run", -1, 50)
    r.col_r.set_inversed(False)
    r.drive(-80, 0, 7, 0, "brake")
    r.turn(-90)
    r.drive(0, 80, 2, 0, "run", 50, 50)


def drop_3(r: Robot):
    direction = r.get_direction_drive(80, 20, 6, 5, "brake")  # Calculate error

    r.turn(90 - direction)

    r.slider.position = 0
    r.slider.open_for_ships(False)
    while r.slider.position < 20:
        time.sleep(0.01)

    r.drive(0, 80, 5, 0, "run", 50, -1)
    r.drive(80, 80, 6.5)

    drop_off(r)

    r.col_l.set_inversed(True)
    r.drive(-80, -80, 6.5, 0, "run", 50, -1)
    r.col_l.set_inversed(False)
    r.drive(-80, 0, 7, 0, "brake")
    r.turn(-90)
    r.drive(0, -80, 4, 0, "run", 50, 50)


def drop_4(r: Robot):
    direction = r.get_direction_drive(80, 100, 0, 5)  # Calculate error
    r.drive_triple(100, 100, 0, 0, 19, 5, 0, "brake")

    r.turn(90 - direction)

    r.slider.position = 0
    r.slider.open_for_ships(False)
    while r.slider.position < 20:
        time.sleep(0.01)

    r.drive(0, 60, 10, 0, "run", 50, 50)

    r.align_driving(60, 80, 0, 2.5)

    drop_off(r)

    r.col_r.set_inversed(True)
    r.col_l.set_inversed(True)
    r.drive(-80, -60, 7, 0, "run", 50, 50)
    direction = r.get_direction_drive(-60, 0, 1.5, 5, "brake")
    r.col_r.set_inversed(False)
    r.col_l.set_inversed(False)

    r.turn(-90 - direction)

    r.drive_triple(0, -100, -80, 5, 10, 3, 0, "run", 50, 50)


def drop_5(r: Robot):
    direction = r.get_direction_drive(80, 100, 0, 5, "run")  # Calculate error
    r.drive_triple(100, 100, 0, 0, 32.5, 5, 0, "brake")

    r.turn(69 - direction)

    r.slider.position = 0
    r.slider.open_for_ships(False)
    while r.slider.position < 20:
        time.sleep(0.01)

    r.drive_triple(0, 60, 60, 5, 5, 5, 25, "run", 50, 50)

    r.drive(60, 80, 3.5, 25)
    r.slider.close(False, 90)
    r.drive_triple(80, 80, 0, 5, 8, 5, 20, "brake")
    r.slider.open_after_ships()

    r.lifter.move_down()

    r.drive_triple(0, -80, -60, 5, 0, 4, 45, "run")

    r.slider.close(False)

    r.col_l.set_inversed(True)
    r.col_r.set_inversed(True)
    direction = r.get_direction_drive(-60, 0, 1, 4, "brake")
    r.col_l.set_inversed(False)
    r.col_r.set_inversed(False)

    r.turn(-90 - direction)
    r.drive_triple(0, -100, -80, 5, 25, 5, 0, "run", 50, 50)


def scan_ships(r: Robot, speed_start=0):
    r.ht_side.mode = 'COLOR'
    r.ht_middle.mode = 'WHITE'
    ships = [MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR, MyColor.NOCOLOR]

    # Move to ship line
    r.slider.close(False)
    line_detected = r.drive(speed_start, 70, 5, 0, "run", 50, 50)

    direction = r.get_direction_drive(70, 0, 10.5, 5, "brake", 90, line_detected)
    r.turn(-90 - direction)

    r.slider.hold_closed()

    # r.drive_triple(0, 100, 0, 5, 0, 5, 0, "brake")
    line_detected = r.drive(0, -70, 3, 0, "run", 50, 50)
    if line_detected:
        r.brake()

    direction = r.get_direction_drive(-70, 0, 0, 5, "brake", line_detected)
    r.turn(-31 - direction, 40, 40, 100, 4, 4)

    r.drive_triple(0, -100, 0, 5, 27, 5, -17, "brake")

    # Align to ship line
    offset = 50
    speed_measure = 100
    speed_maximum = 100

    r.line_follow(50, 70, 4, offset, "run", False, False, False, 2)
    r.line_follow(70,  80, 15, offset, "run", False, False, True, 2)
    r.line_follow(80, 50, 13, offset, "brake", False, False, False, 1)
    r.drive_triple(0, -100, -100, 5, 12, 0)
    # r.drive(0, -80, 15)
    r.drive_color(-100, -20, 15, 0, "brake", False, True)

    # Start ship scanning

    # first ship
    r.line_follow(40, speed_measure, 5, offset, "run")

    color = r.ht_side.get_color()
    print(color.name)
    print(r.ht_side.value())
    ships[0] = color

    # second ship
    ships[1] = next_ship(r, offset, speed_measure, speed_maximum)

    # third ship
    r.line_follow(speed_measure, speed_maximum, 15, offset, "run", False, False, True)
    r.drive(speed_maximum, speed_measure, 6.5, 0, "run")
    # time.sleep(5)

    color = r.ht_side.get_color()
    print(color.name)
    print(r.ht_side.value())
    ships[2] = color

    # forth ship
    ships[3] = next_ship(r, offset, speed_measure, speed_maximum)
    # fifth ship
    ships[4] = next_ship(r, offset, r.consts.drive_min_speed, speed_maximum)
    ships[5] = MyColor.NOCOLOR

    # Move to center
    # r.drive(0, -100, 7, -30)
    # r.drive(-100, -100, 2)
    # r.drive(-100, 0, 7, 30, "brake")

    # r.pivot(-90)
    r.turn(-100)
    return ships


def drop_off(r: Robot, speed_end=-80):
    r.slider.stop(stop_action='brake')
    r.slider.close(False)
    r.drive_triple(80, 80, 0, 5, 7, 5, 0, "brake")

    r.slider.open_after_ships()

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

    line_detected = r.drive(0, 80, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(80, 0, 0, 3, "brake", 90, line_detected)
    r.turn(-direction)

    # r.drive(0, -100, 5, 0, "run", 50)
    # r.drive_triple(-100, -100, 0, 2, 2, 5, 0, "brake")
    line_detected = r.drive(0, -80, 1, 0, "run", 50, 50)
    direction = r.get_direction_drive(-80, 0, 5.5, 3, "brake", 90, line_detected)

    r.turn(90 - direction)

    position = True     # True = In front of line; False = behind line
    # speed_start = 0
    r.drive(0, -80, 5, 0, "run", 50, 50)
    i = 0
    while i < 3:
        destination = positions[i]
        r.slider.hold_closed()
        if position:
            # r.drive(-speed_start, -80, 5, 0, "run", 50, 50)
            position = False

            if target_position(destination):
                direction = r.get_direction_drive(-80, -50, 0, 5, "brake")  # Calculate error
                r.turn(-direction)
                r.drive(0, 80, 2, 0, "run", 50, 50)
                i -= 1
            else:
                if destination is 2:
                    drop_2(r)
                elif destination is 1:
                    drop_1(r)
                else:   # destination is 0
                    drop_0(r)
        else:
            # r.drive(speed_start, 80, 3, 0, "run", 50, 50)
            position = True

            if not target_position(destination):
                direction = r.get_direction_drive(80, 20, 0, 5, "brake")  # Calculate error
                r.turn(-direction)
                r.drive(0, -80, 2, 0, "run", 50, 50)
                i -= 1
            else:
                if destination is 3:
                    drop_3(r)
                elif destination is 4:
                    drop_4(r)
                else:   # destination is 5
                    drop_5(r)
        i += 1

    if position:
        line_detected = r.drive(0, -80, 5, 0, "run", 50, 50)
        direction = r.get_direction_drive(-80, -20, 2, 5, "brake", 90, line_detected)  # Calculate error
        r.turn(-direction)

    line_detected = r.drive(0, 80, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(80, 50, 0, 3, "brake", line_detected)  # Calculate error
    r.turn(90 - direction)


def get_free_ship_position(r: Robot):
    occupied = r.ship_positions
    for i in [2, 3, 1, 4]:
        if i not in occupied:
            return i


def z_drop_drive(r: Robot):
    r.drive_triple(0, 100, 0, 2.5, 0, 2.5, 0, "brake")


def z_drop_drive_rev(r: Robot):
    r.drive_triple(0, -100, 0, 2.5, 0, 2.5, 0, "brake")


def z_part__drop(r: Robot):
    r.drive(0, -80, 5, 0, "run", 50, 50)
    position = True
    finished = False
    destination = get_free_ship_position(r)
    while not finished:
        if position:
            # r.drive(-speed_start, -80, 5, 0, "run", 50, 50)
            position = False

            if target_position(destination):
                direction = r.get_direction_drive(-80, -50, 0, 5, "brake")  # Calculate error
                r.turn(-direction)
                r.drive(0, 80, 2, 0, "run", 50, 50)
                finished = False
            else:
                finished = True
                if destination is 2:
                    direction = r.get_direction_drive(-80, -20, 1, 5, "brake")  # Calculate error

                    r.turn(90 - direction)
                    z_drop_drive(r)
                    r.lifter.z_move_down()
                    z_drop_drive_rev()
                    r.turn(-90)
                    r.slider.close(False)
                    r.drive(0, 80, 2, 0, "run", 50, 50)
                elif destination is 1:
                    direction = r.get_direction_drive(-80, -100, 0, 5)  # Calculate error
                    r.drive_triple(-100, -100, 0, 0, 14, 5, 0, "brake")

                    r.turn(90 - direction)
                    z_drop_drive(r)
                    r.lifter.z_move_down()
                    z_drop_drive_rev()
                    r.turn(-90)
                    r.slider.close(False)
                    r.drive_triple(0, 100, 80, 5, 10, 3, 0, "run", 50, 50)
        else:
            # r.drive(speed_start, 80, 3, 0, "run", 50, 50)
            position = True

            if not target_position(destination):
                direction = r.get_direction_drive(80, 20, 0, 5, "brake")  # Calculate error
                r.turn(-direction)
                r.drive(0, -80, 2, 0, "run", 50, 50)
                finished = False
            else:
                finished = True
                if destination is 3:
                    direction = r.get_direction_drive(80, 20, 6, 5, "brake")  # Calculate error

                    r.turn(90 - direction)
                    z_drop_drive(r)
                    r.lifter.z_move_down()
                    z_drop_drive_rev()
                    r.turn(-90)
                    r.slider.close(False)
                    r.drive(0, -80, 4, 0, "run", 50, 50)
                elif destination is 4:
                    direction = r.get_direction_drive(80, 100, 0, 5)  # Calculate error
                    r.drive_triple(100, 100, 0, 0, 19, 5, 0, "brake")

                    r.turn(90 - direction)
                    z_drop_drive(r)
                    r.lifter.z_move_down()
                    z_drop_drive_rev()
                    r.turn(-90)
                    r.slider.close(False)

                    r.drive_triple(0, -100, -80, 5, 10, 3, 0, "run", 50, 50)
    if position:
        line_detected = r.drive(0, -80, 5, 0, "run", 50, 50)
        direction = r.get_direction_drive(-80, -20, 2, 5, "brake", 90, line_detected)  # Calculate error
        r.turn(-direction)

    line_detected = r.drive(0, 80, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(80, 50, 0, 3, "brake", line_detected)  # Calculate error
    r.turn(90 - direction)


def z_main(r: Robot):
    r.slider.open_for_base(False)
    line_detected = r.drive(0, -80, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(-80, 0, 0, 5, "brake", 90, line_detected)  # Calculate error
    r.turn(-direction)

    r.drive_triple(0, -100, -100, 8, 75, 5, 0, "run")

    direction = r.get_direction_drive(-100, 0, 40, 5, "brake", 3)

    r.turn(-90 - direction)
    r.drive_triple(0, 100, 100, 5, 18, 0)
    r.drive(100, 100, 10, 0, "run", 0, 50)
    r.drive_time(100, 0, 7, 0, "brake", 1)

    r.lifter.z_move_up_partly(False)
    # time.sleep(0.5)
    r.drive(0, -100, 10, 0, "run", 0, 50)
    r.drive_triple(-100, -100, 0, 5, 31.5, 5, 0, "brake")
    r.lifter.move_up(False)
    r.turn(90)

    r.drive_triple(0, 100, 10, 15, 10, 5, 0, "brake")

    r.drive(100, 100, 40, 0, "run", 50, 50)

    r.drive_triple(0, 100, 100, 5, 10, 10, 0, "run", 50, 50)
    # transition

    r.drive(100, 100, 45, -16)
    r.drive(100, 100, 5)
    r.drive(100, 100, 45, 16)

    line_detected = r.drive(100, 70, 5, 0, "run", 50, 50)

    direction = r.get_direction_drive(70, 0, 10.5, 5, "brake", 90, line_detected)
    r.turn(-90 - direction)

    z_part__drop(r)
    # direction = r.get_direction_drive(80, 80, 100, 10, "run", 1)  # Calculate error

    # r.drive_wall(50, 100, 1, -20, "run", 0, 50)
    # r.drive_wall(100, 100, 15, -25)
    # r.drive_wall(100, 60, 5, -25)
    # r.drive_wall(60, 50, 20, -10, "run", 30, 30)
    # r.drive_wall(50, 70, 4, -7)
    # r.slider.run_to_rel_pos(position_sp=10, speed_sp=100)
    # # r.slider.run_direct(duty_cycle_sp=30)
    # r.drive_wall(70, 0, 6.4, -1, "brake")


def go_home_bitch(r: Robot):
    r.slider.open_for_base(False)
    line_detected = r.drive(0, -80, 3, 0, "run", 50, 50)
    direction = r.get_direction_drive(-80, 0, 0, 5, "brake", 90, line_detected)  # Calculate error
    r.turn(-direction)

    r.drive_triple(0, -100, -100, 8, 75, 5, 0, "run")

    direction = r.get_direction_drive(-100, 0, 38, 5, "brake", 3)

    r.turn(-75 - direction)
    r.drive_wall(0, -100, 3)
    r.drive_wall(-100, -100, 32)
    r.drive_wall(-100, -100, 10, 0, "run", 0, 50)
    r.drive_wall(-100, 0, 2, 0, "run")

    r.drive_wall(50, 100, 1, -20, "run", 0, 50)
    r.drive_wall(100, 100, 15, -25)
    r.drive_wall(100, 60, 5, -25)
    r.drive_wall(60, 50, 20, -10, "run", 30, 30)
    r.drive_wall(50, 70, 4, -7)
    r.slider.run_to_rel_pos(position_sp=10, speed_sp=100)
    # r.slider.run_direct(duty_cycle_sp=30)
    r.drive_wall(70, 0, 6, -1, "brake")


def run(r: Robot, speed_start=0):
    r.lifter.move_to_top_position(False)

    ships = scan_ships(r, speed_start)

    container = r.container_colors
    # container = [MyColor.BLUE, MyColor.GREEN, MyColor.YELLOW]

    positions = get_positions(ships, container)
    r.ship_positions = positions
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
