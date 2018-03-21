#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
from robot import MyColor
import time


def target_position(color):
    if color is MyColor.RED or color is MyColor.YELLOW:
        return True
    return False


def pick_up(robot: Robot, i):
    robot.slider.open_for_lifter()
    robot.drive_triple(0, 50, 50, 6, 20, 20, 0, "run", 50, 50)  # move to line

    if i is 0:
        robot.drive(50, 0, 5, 0, "brake")

        robot.speak(str(i))
        robot.lifter.move_up()

        robot.slider.close()

        robot.drive_triple(0, -60, -60, 6, 10, 10, 0, "run", 50, 50)    # Move to line
        robot.drive(-60, 0, 10, 0, "brake")

        robot.reset_motor_pos()
        robot.drive_triple(0, 50, 0, 2, 0, 1, 0, "brake")

        robot.slider.open()
        robot.drive_triple(0, -50, 0, 7, 1, 2, 0, "brake")
        robot.slider.close()
    elif i is 1:
        robot.drive(50, 0, 7.5, 0, "brake")

        robot.speak(str(i))
        robot.lifter.move_up()

        robot.slider.close()

        robot.reset_motor_pos()
        robot.drive_triple(0, -40, 0, 2.5, 3, 1, 0, "brake")

        robot.slider.open_to_half()
        robot.drive_triple(0, -50, 0, 4, 11, 3, 0, "brake")
        robot.slider.close()
    elif i is 2:
        robot.drive(50, 0, 8, 0, "brake")

        robot.slider.close(False, 20, 1)
        robot.speak(str(i))
        robot.lifter.move_up()

        robot.slider.close()

        robot.reset_motor_pos()
        robot.drive_triple(0, -40, 0, 2, 4, 2, 0, "brake")

        robot.slider.open_to_half()
        robot.drive_triple(0, -50, 0, 3, 12, 3, 0, "brake")
        robot.slider.close()


def run(r: Robot, speed_start=0):
        colors = [MyColor.GREEN, MyColor.YELLOW, MyColor.RED, MyColor.GREEN]
        # r.container_colors[0]
        position = True     # True = In front of line; False = behind line
        i = 0
        while i < 3:
            color = colors[i]
            if position:
                r.drive(speed_start, -60, 5, 0, "run", 50, 50)
                speed_start = 0
                position = False
                if target_position(color):
                    r.align_driving(-60, -20, 3, 6, "brake")
                    i -= 1
                else:
                    r.align_driving(-60, -20, 0, 5)
                    if color is MyColor.GREEN:
                        r.pivot(90, False, 30)
                        pick_up(r, i)
                        r.pivot(-90, False, -20, 50)
                    else:   # blue
                        r.pivot(-90, False, 30)
                        pick_up(r, i)
                        r.pivot(90, False, -20, 50)
            else:
                r.drive(20, 60, 3, 0, "run", 50, 50)
                position = True
                if not target_position(color):
                    r.align_driving(60, 20, 2, 5, "brake")
                    i -= 1
                else:
                    r.align_driving(60, 0, 18, 10.5, "brake")
                    if color is MyColor.RED:
                        r.pivot(90, False, 30)
                        pick_up(r, i)
                        r.pivot(-90, False, -20, 50)
                    else:   # Yellow
                        r.pivot(-90, False, 30)
                        pick_up(r, i)
                        r.pivot(90, False, -20, 50)
            i += 1


def run_old(r: Robot, speed_start=0):       # Deprecated
    colors = [MyColor.GREEN, MyColor.YELLOW, MyColor.RED, MyColor.GREEN]
    # r.container_colors[0]
    position = True  # True = In front of line; False = behind line
    i = 0
    while i < 3:
        color = colors[i]
        if position:
            r.drive(speed_start, -60, 5, 0, "run", 50, 50)
            speed_start = 0
            position = False
            if target_position(color):
                r.align_driving(-60, -20, 3, 6, "brake")
                i -= 1
            else:
                r.align_driving(-60, -20, 0, 5)
                if color is MyColor.GREEN:
                    r.pivot(90, False, 30)
                    pick_up(r, i)
                    r.pivot(-90, False, -20, 50)
                else:  # blue
                    r.pivot(-90, False, 30)
                    pick_up(r, i)
                    r.pivot(90, False, -20, 50)
        else:
            r.drive(20, 60, 3, 0, "run", 50, 50)
            position = True
            if not target_position(color):
                r.align_driving(60, 20, 2, 5, "brake")
                i -= 1
            else:
                r.align_driving(60, 0, 18, 10.5, "brake")
                if color is MyColor.RED:
                    r.pivot(90, False, 30)
                    pick_up(r, i)
                    r.pivot(-90, False, -20, 50)
                else:  # Yellow
                    r.pivot(-90, False, 30)
                    pick_up(r, i)
                    r.pivot(90, False, -20, 50)
        i += 1


if __name__ == "__main__":
    rob = Robot()
    try:
        print("PART 2")
        run(rob)
    finally:
        print("RESET")
        rob.reset()
        time.sleep(0.5)
