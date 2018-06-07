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
    robot.slider.run_to_abs_pos(position_sp=260, speed_sp=1000, stop_action="brake")

    while robot.slider.position < 10:
        time.sleep(0.01)
    # time.sleep(0.3)
    line_detected = robot.drive_triple(0, 80, 80, 4, 4.5, 0, 0, "run", 50, 50)
    # line_detected = robot.drive(0, 80, 10, 0, "run", 50, 50)
    robot.lifter.move_up(False)

    if not line_detected:
        line_detected = robot.drive(80, 80, 5.5, 0, "run", 50, 50)

    robot.slider.run_to_abs_pos(position_sp=10, speed_sp=900, stop_action="brake")
    # robot.slider.close(False, 100, 11)

    if not line_detected:
        robot.drive(80, 80, 40, 0, "run", 50, 50)

    if i is 0:
        robot.drive(80, 0, 5, 0, "brake")

        # time.sleep(0.5)
        robot.slider.wait_while('running', 500)
        robot.slider.hold_closed()

        robot.drive_triple(0, -80, -80, 5, 10, 10, 0, "run", 50, 50)    # Move to line
        robot.drive(-80, 0, 11, 0, "brake")

        robot.drive_triple(0, 60, 0, 3, 0, 2.5, 0, "brake")

        robot.slider.open_to_half()
        robot.drive_triple(0, -100, 0, 7, 7, 2, 0, "brake")
    elif i is 1:
        robot.drive(80, 0, 7.5, 0, "brake")

        robot.slider.wait_while('running', 500)
        robot.slider.hold_closed()

        # time.sleep(0.5)

        robot.drive_triple(0, -70, 0, 3, 0, 3, 0, "brake", 50, 50)

        robot.slider.open_to_half()
        robot.drive_triple(0, -100, 0, 5, 14, 5, 0, "brake")
    elif i is 2:
        robot.drive(80, 0, 9, 0, "brake")

        robot.slider.wait_while('running', 500)
        robot.slider.hold_closed()

        robot.drive_triple(0, -80, 0, 4, 0, 3.5, 0, "brake")

        robot.slider.open_to_half()
        robot.drive_triple(0, -100, 0, 5, 14, 5, 0, "brake")

    else:
        return

    # robot.slider.run_to_abs_pos(position_sp=220, speed_sp=1000)
    robot.slider.run_forever(speed_sp=-1000)
    while robot.slider.position >= 220:
        time.sleep(0.01)
    # robot.slider.wait_while('running', 1000)
    # robot.slider.close(False)
    # position = robot.slider.position
    # robot.slider.run_timed(time_sp=1300, speed_sp=-1000)
    # while robot.slider.position >= position - 400:
    #       time.sleep(0.01)


def run(r: Robot, speed_start=0):
    print("PART2")
    colors = r.container_colors
    # colors = [MyColor.BLUE, MyColor.RED, MyColor.GREEN]
    position = True     # True = In front of line; False = behind line
    i = 0
    while i < 3:
        color = colors[2-i]     # LIFO
        print("color:" + color.to_text())
        r.slider.hold_closed()
        if position:
            r.drive(speed_start, -70, 5, 0, "run", 50, 50)
            speed_start = 0
            position = False
            if target_position(color):
                direction = r.get_direction_drive(-70, -50, 3, 4, "brake")  # Calculate error
                r.turn(-direction)
                i -= 1
            else:
                direction = r.get_direction_drive(-70, -100, 0, 4)  # Calculate error

                if color is MyColor.GREEN:
                    r.drive_triple(-100, -100, -50, 2, 0, 7.5, 0, "brake")

                    r.slider.position = 0
                    r.slider.run_forever(speed_sp=100)

                    r.turn(-90 - direction, 40, 40, 100, 4, 4)
                    pick_up(r, i)
                    r.turn(90)
                else:   # blue
                    r.drive_triple(-100, -100, -50, 2, 0, 6, 0, "brake")

                    r.slider.position = 0
                    r.slider.run_forever(speed_sp=100)

                    r.turn(90 - direction, 40, 40, 100, 4, 4)
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
                # direction = r.get_direction_drive(70, 50, 8.5, 10, "brake")  # Calculate error
                direction = r.get_direction_drive(70, 100, 0, 4, "brake")  # Calculate error

                if color is MyColor.RED:
                    r.drive_triple(100, 100, 50, 2, 7, 5, 0, "brake")

                    r.slider.position = 0
                    r.slider.run_forever(speed_sp=100)
                    r.turn(-90 - direction, 40, 40, 100, 4, 4)
                    pick_up(r, i)
                    r.turn(90)
                else:   # Yellow
                    r.drive_triple(100, 100, 50, 2, 8, 5, 0, "brake")

                    r.slider.position = 0
                    r.slider.run_forever(speed_sp=100)
                    r.turn(88 - direction, 40, 40, 100, 4, 4)
                    pick_up(r, i)
                    r.turn(-90)
        i += 1

    if position:
        r.drive(speed_start, -70, 5, 0, "run", 50, 50)
        direction = r.get_direction_drive(-70, -20, 3, 6, "brake")  # Calculate error
        r.turn(-direction)


def transition(r: Robot):
    r.drive_triple(0, 100, 100, 5, 10, 10, 0, "run", 50, 50)
    # r.align_driving(80, 100, 0, 7)
    r.drive(100, 100, 45, -18)
    # direction = r.get_direction_drive(80, 20, 2, 5, "brake")  # Calculate error
    # r.turn(-direction)

    # r.drive_triple(0, 100, 100, 5, 2, 2, -20)
    r.drive(100, 100, 5)
    # r.drive_triple(100, 100, 0, 2, 2, 5, 20, "brake")
    r.drive(100, 100, 45, 18)


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 2")
        run(rob)
    finally:
        print("RESEsT")
        rob.reset()
        time.sleep(0.5)
