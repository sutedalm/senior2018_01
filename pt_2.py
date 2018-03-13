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


def pick_up(robot, i):
    robot.drive(80, 0, 5, 0, "hold")
    robot.speak(str(i))


def run(r):
        colors = [MyColor.RED, MyColor.BLUE, MyColor.YELLOW, MyColor.GREEN]
        # r.container_colors[0]
        position = True     # True = In front of line; False = behind line
        # TODO: Change Speed at start
        i = 0
        while i < 4:    # TODO: Change to 3
            color = colors[i]
            if position:
                r.drive(0, -60, 5)
                position = False
                if target_position(color):
                    # r.speak("FAIL")
                    r.align_driving(-60, -20, 7, "hold")
                    i -= 1
                else:
                    r.align_driving(-60, -30, 23)
                    if color is MyColor.GREEN:
                        r.pivot(-90, True, 30)
                        r.drive(0, 80, 5)
                        r.move_to_line(80)
                        pick_up(r, i)
                        r.drive_triple(0, -80, -20, 6, 6, 6)
                        r.pivot(-90, False, -20, 50)
                    else:   # -blue
                        r.pivot(90, True, 30)
                        r.drive(0, 80, 5)
                        r.move_to_line(80)
                        pick_up(r, i)
                        r.drive_triple(0, -80, -20, 6, 6, 6)
                        r.pivot(90, False, -20, 50)
            else:
                r.drive(20, 60, 3)
                position = True
                if not target_position(color):
                    r.align_driving(60, 20, 7, "hold")
                    i -= 1
                else:
                    r.align_driving(60, 30, 7.5, "hold")
                    if color is MyColor.RED:
                        r.pivot(-90, True, 30)
                        r.drive(0, 80, 5)
                        r.move_to_line(80)
                        pick_up(r, i)
                        r.drive_triple(0, -80, -20, 6, 6, 6)
                        r.pivot(-90, False, -20, 50)
                    else:   # Yellow
                        r.pivot(90, True, 30)
                        r.drive(0, 80, 5)
                        r.move_to_line(80)
                        pick_up(r, i)
                        r.drive_triple(0, -80, -20, 6, 6, 6)
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
