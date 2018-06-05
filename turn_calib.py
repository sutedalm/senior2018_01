#!/usr/bin/env python3

from robot import Robot
from robot import RobotConstants
import time
from math import  pi

def main(r: Robot):
    distances = []
    iterations = 5
    for i in range(0, iterations):
        r.reset()
        r._lMot.reset()
        r._rMot.reset()

        kp = RobotConstants.turn_kp
        ki = RobotConstants.turn_ki
        kd = RobotConstants.turn_kd

        line_crossings = 0
        on_line = False
        start_reached = False
        target_reached = False

        start_distance = 0
        end_distance = 0

        print("TURNING")
        driven_distance = 0

        last_error = integral = 0

        r._lMot.duty_cycle_sp = r._rMot.duty_cycle_sp = 0
        r._lMot.run_direct()
        r._rMot.run_direct()

        while not target_reached:

            l_pos = r._lMot.position
            r_pos = r._rMot.position

            driven_distance = abs(l_pos) + abs(r_pos)
            speed = RobotConstants.drive_min_speed

            error = abs(l_pos) - abs(r_pos)
            integral, last_error, correction = r._util.pid(error, integral, last_error, kp, ki, kd)

            if on_line and r.col_l.light_reflected() > 50:
                on_line = False
            elif (not on_line) and (r.col_l.light_reflected() < 50):
                on_line = True
                line_crossings += 1

            if line_crossings >= 1 and not start_reached:
                start_reached = True
                start_distance = driven_distance

            if line_crossings >= 3 and not target_reached:
                target_reached = True
                end_distance = driven_distance

            r._rMot.duty_cycle_sp = r._util.clamp_speed(-speed - correction)
            r._lMot.duty_cycle_sp = r._util.clamp_speed(speed - correction)

        r._lMot.stop(stop_action="brake")
        r._rMot.stop(stop_action="brake")

        driven_distance = r._util.deg_to_cm(end_distance - start_distance)
        motor_distance = driven_distance / (2 * pi)
        print("Motor Distance: " + str(motor_distance))
        distances.append(motor_distance)
        r.reset()
        r.turn(-90)
        time.sleep(0.5)

    avg = 0
    for i in distances:
        avg += i
    avg /= iterations
    print("avgerage motor distance: " + str(avg))
    r.wait_until_button()


if __name__ == "__main__":
    r = Robot()
    try:
        print("TURN CALIB")
        main(r)
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)
