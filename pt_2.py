#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
from robot import MyColor
import time


def target_position(color):
    if color in {MyColor.RED, MyColor.YELLOW}:
        return True
    return False


def pick_up(robot: Robot, i):
    # robot.drive_triple(0, 50, 50, 4, 0, 0, 0, "brake", 50, 50)  # move to line
    robot.slider.open_for_lifter(False)
    time.sleep(0.3)
    robot.drive_triple(0, 60, 80, 40, 20, 20, 0, "run", 50, 50)  # move to line

    if i is 0:
        robot.lifter.move_up(False)
        robot.drive(80, 0, 5, 0, "brake")

        # time.sleep(0.5)

        robot.slider.close()

        robot.drive_triple(0, -80, -100, 5, 10, 10, 0, "run", 50, 50)    # Move to line
        robot.drive(-100, 0, 11, 0, "brake")

        # robot.reset_motor_pos()
        robot.drive_triple(0, 70, 0, 3, 0, 2, 0, "brake")

        robot.slider.open_to_half()
        robot.drive_triple(0, -80, 0, 7, 7, 2, 0, "brake")
    elif i is 1:
        robot.lifter.move_up(False)
        robot.drive(80, 0, 7.5, 0, "brake")

        # time.sleep(0.5)

        robot.slider.close()

        # robot.reset_motor_pos()
        robot.drive_triple(0, -80, 0, 3.5, 0, 2, 0, "brake", 50, 50)

        robot.slider.open_to_half()
        robot.drive_triple(0, -80, 0, 5, 14, 5, 0, "brake")
    elif i is 2:
        # robot.slider.close(False, 20, 1)

        robot.lifter.move_up(False)
        robot.drive(80, 0, 9, 0, "brake")
        # time.sleep(0.5)

        robot.slider.close()

        # robot.reset_motor_pos()
        robot.drive_triple(0, -80, 0, 4, 0, 3, 0, "brake")

        robot.slider.open_to_half()
        robot.drive_triple(0, -80, 0, 5, 14, 5, 0, "brake")

    robot.slider.close(False)
    time.sleep(0.5)


def run(r: Robot, speed_start=0):
    print("PART2")
    colors = r.container_colors
    # TODO: Color detection error correction
    # colors = [MyColor.BLUE, MyColor.RED, MyColor.GREEN]
    position = True     # True = In front of line; False = behind line
    i = 0
    while i < 3:
        color = colors[2-i]     # LIFO
        r.slider.hold_closed()
        if position:
            r.drive(speed_start, -70, 5, 0, "run", 50, 50)
            speed_start = 0
            position = False
            if target_position(color):
                direction = r.get_direction_drive(-70, -50, 3, 6, "brake")  # Calculate error
                r.turn(-direction)
                i -= 1
            else:
                # TODO: separate get_direction_drive in individual colors
                direction = r.get_direction_drive(-70, -50, 4, 9, "brake")  # Calculate error
                if color is MyColor.GREEN:
                    r.turn(-90 - direction)
                    pick_up(r, i)
                    r.turn(90)
                else:   # blue
                    r.turn(90 - direction)
                    pick_up(r, i)
                    r.turn(-90)
        else:
            r.drive(0, 70, 3, 0, "run", 50, 50)
            position = True
            if not target_position(color):
                direction = r.get_direction_drive(70, 50, 3, 6, "brake")  # Calculate error
                r.turn(-direction)
                i -= 1
            else:
                direction = r.get_direction_drive(70, 50, 8.5, 10, "brake")  # Calculate error
                if color is MyColor.RED:
                    r.turn(-90 - direction)
                    pick_up(r, i)
                    r.turn(90)
                else:   # Yellow
                    r.turn(90 - direction)
                    pick_up(r, i)
                    r.turn(-90)
        i += 1

    if position:
        r.drive(speed_start, -70, 5, 0, "run", 50, 50)
        direction = r.get_direction_drive(-70, -20, 3, 6, "brake")  # Calculate error
        r.turn(-direction)

    r.drive_triple(0, 100, 100, 5, 10, 10, 0, "run", 50, 50)
    # r.align_driving(80, 100, 0, 7)
    r.drive(100, 100, 45, -15)
    # direction = r.get_direction_drive(80, 20, 2, 5, "brake")  # Calculate error
    # r.turn(-direction)

    # r.drive_triple(0, 100, 100, 5, 2, 2, -20)
    r.drive(100, 100, 5)
    # r.drive_triple(100, 100, 0, 2, 2, 5, 20, "brake")
    r.drive(100, 100, 45, 15)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 2")
        run(rob)
    finally:
        print("RESEsT")
        rob.reset()
        time.sleep(0.5)
