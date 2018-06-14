#!/usr/bin/env python3

from robot import Robot
import time


def main():
    r = Robot()
    try:
        left_pressed = False
        right_pressed = False
        middle_pressed = False
        while not r.btn.backspace:
            if r.btn.up:
                r.beep()
                time.sleep(1)
                r.reset_motor_pos()
                r.turn(90)
            elif r.btn.down:
                r.beep()
                time.sleep(1)
                r.reset_motor_pos()
                r.turn(-90)

            if r.btn.left and not left_pressed:
                r.consts.motor_distance_turn += 0.05
                print("")
                print(str(r.consts.motor_distance_turn))
                left_pressed = True
            if not r.btn.left and left_pressed:
                left_pressed = False

            if r.btn.right and not right_pressed:
                r.consts.motor_distance_turn -= 0.05
                print("")
                print(str(r.consts.motor_distance_turn))
                right_pressed = True
            if not r.btn.right and right_pressed:
                right_pressed = False

            if r.btn.enter and not middle_pressed:
                print(str(r.consts.motor_distance_turn))
                middle_pressed = True
            if not r.btn.enter and middle_pressed:
                middle_pressed = False

    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
