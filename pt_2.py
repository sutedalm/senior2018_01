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
    # robot.speak(str(i))
    robot.drive_triple(0, 80, 80, 6, 10, 10, 0, "run", 50, 50)  # move to line

    if i is 0:
        robot.drive(80, 0, 5, 0, "hold")

        robot.speak(str(i))
        time.sleep(1)       # pick up temperature controller

        robot.drive_triple(0, -60, -60, 6, 10, 10, 0, "run", 50, 50)    # Move to line
        robot.drive(-60, 0, 10, 0, "hold")

        robot.drive_triple(0, 50, 0, 2.5, 0, 1, 0, "hold")

        robot.slider.open()
        robot.drive_triple(0, -30, 0, 8, 0, 2, 0, "hold")
        robot.slider.close()
    elif i is 1:
        robot.drive(80, 0, 7, 0, "hold")

        robot.speak(str(i))
        time.sleep(1)

        robot.drive_triple(0, -40, 0, 2, 3, 1, 0, "hold")

        robot.slider.open_to_half()
        robot.drive_triple(0, -50, 0, 4, 11, 3, 0, "hold")
        robot.slider.close()
    elif i is 2:
        robot.drive(80, 0, 8, 0, "hold")

        robot.speak(str(i))
        time.sleep(1)

        robot.drive_triple(0, -40, 0, 2, 4, 2, 0, "hold")

        robot.slider.open_to_half()
        robot.drive_triple(0, -50, 0, 3, 12, 3, 0, "hold")
        robot.slider.close()


def run(r: Robot):
        colors = [MyColor.YELLOW, MyColor.BLUE, MyColor.GREEN, MyColor.GREEN]
        # r.container_colors[0]
        position = True     # True = In front of line; False = behind line
        # TODO: Change Speed at start
        i = 0
        while i < 3:
            color = colors[i]
            if position:
                r.drive(0, -60, 5)
                position = False
                if target_position(color):
                    r.align_driving(-60, -20, 2, 5, "hold")
                    i -= 1
                else:
                    r.align_driving(-60, -30, 12.5, 10, "hold")
                    if color is MyColor.GREEN:
                        r.pivot(-90, True, 30)
                        pick_up(r, i)
                        r.pivot(-90, False, -20, 50)
                    else:   # blue
                        r.pivot(90, True, 30)
                        pick_up(r, i)
                        r.pivot(90, False, -20, 50)
            else:
                r.drive(20, 60, 3)
                position = True
                if not target_position(color):
                    r.align_driving(60, 20, 2, 5, "hold")
                    i -= 1
                else:
                    r.align_driving(60, 30, 2, 5.5)
                    if color is MyColor.RED:
                        r.pivot(-90, True, 30)
                        pick_up(r, i)
                        r.pivot(-90, False, -20, 50)
                    else:   # Yellow
                        r.pivot(90, True, 30)
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
