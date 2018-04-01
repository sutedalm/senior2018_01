#!/usr/bin/env python3

"""
http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
https://github.com/Klabbedi/ev3
"""
from robot import Robot
import pt_1
import pt_2
import pt_3
import time


def festhalte_test(r: Robot):
        r.slider.close()
        r.drive_triple(0, 60, 0, 5, 20, 5, 0, "brake")
        r.slider.open()
        r.drive_triple(0, -60, 0, 5, 10, 5, 0, "brake")
        r.slider.close()
        r.drive_triple(0, -60, 0, 5, 10, 5, 0, "brake")


def testing(r: Robot):
    # r.drive_triple(0, 50, 0, 10, 10, 10, 0, "brake")
    # r.drive_triple(0, 50, 0, 10, 10, 10, 0, "brake")
    # r.drive(0, 60, 5, 0, "run", 50, 50)
    # r.align_driving(60, 0, 3, 5, "brake")
    # r.drive(30, 30, 4, 0, "brake")
    #
    # r.lifter.move_up()
    # r.lifter.move_up()
    # r.lifter.move_up()
    #
    # time.sleep(1)
    #
    # r.drive(30, 30, 4, 0, "brake")
    #
    # r.lifter.move_down()
    # r.lifter.move_down()
    # r.lifter.move_down()
    # r.drive(0, 20, 5)
    # r.get_direction(20)
    # r.pivot(-90, True)
    # r.drive_triple(0, 100, 0, 10, 5, 15, 0, "brake")
    # r.pivot(90, False)
    # r.drive_triple(-20, -100, -20, 20, 5, 20, 0, "hold")
    # r.drive_triple(0, 80, 0, 10, 1, 10, 0, "brake")
    # r.pivot(90, True)
    # r.pivot(-90, False)
    # r.pivot(-90, False)

    # r.lifter.move_up()
    # time.sleep(2)
    # r.lifter.move_up()
    # time.sleep(2)
    # r.lifter.move_up()
    # time.sleep(2)
    # r.lifter.move_down()
    # time.sleep(2)
    # r.lifter.move_down()
    # time.sleep(2)
    # r.lifter.move_down()
    # time.sleep(2)

    # r.ht_middle.mode = 'WHITE'
    # while True:
    #     print(str(r.ht_middle.light_reflected()))
        # a = r.ht_middle.value(0)
        # b = r.ht_middle.value(1)
        # c = r.ht_middle.value(2)
        # d = r.ht_middle.value(3)
        # print(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d))

    # r.turn(360)
    # r.turn(-90)
    # print("l: " + str(r._lMot.position) + "; r: " + str(r._rMot.position))

    # while True:
    #     color = r.ht_middle.get_color()
    #     r.speak(color.to_text())
    #     r.wait_until_button()
    # print(str(r.lifter.position))
    #
    # r.lifter.move_to_top_position(False)
    # print(str(r.lifter.position))
    # time.sleep(3)
    # r.lifter.move_to_first_position(False)
    # time.sleep(3)

    # direction = r.get_direction_drive(80, 20, 8.5, 10, "brake")  # Calculate error
    # r.turn(-90 - direction)

    # r.ht_middle.mode = 'WHITE'
    # r.line_follow(30, 30, 100, 50, "run")
    # r.ht_side.mode = 'COLOR'
    # while True:
    #     print(r.ht_side.get_color().to_text())
    #     print(r.ht_side.value())

    # r.drive_triple(0, -100, 0, 5, 5, 5, 0, "brake")
    # time.sleep(2)
    # print(str(r._lMot.position) + ' ' + str(r._rMot.position))
    # r.reset_motor_pos()
    # r.turn(90)
    #
    # r.drive(0, 60, 5, 0, "run", 50, 50)
    # r.align()
    # pt_3.drop_off(r, 0, 0)

    r.ht_middle.mode = 'WHITE'
    while True:
        print(str(r.ht_middle.value()) + ' ' + str(r.ht_middle.light_reflected()))


def main():
    r = Robot()
    try:
        print("running")
        r.beep(True)
        time.sleep(2)
        r.ht_middle.mode = 'COLOR'

        # testing(r)

        pt_1.run(r)
        pt_2.run(r, -60)  # change to -60
        pt_3.run(r)
        # r.lifter.move_to_first_position()
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
