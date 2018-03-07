from ev3dev.auto import *
import os
import math

class MyColorSensorEV3:
    def __init__(self, port=INPUT_1, min_val=0, max_val=100):
        self._col = ColorSensor(port)
        self._min_val = min_val
        self._max_val = max_val
        self._col.mode = 'COL-REFLECT'

    def light_reflected(self):
        if self._col.mode is not 'COL-REFLECT':
            self._col.mode = 'COL-REFLECT'
        val = self._col.value()/(self._max_val-self._min_val) * 100
        val = min(100, val)
        val = max(0, val)
        return val


class Robot:
    _tyre_size = 6.24               # Durchmesser des Motors in cm
    _motor_distance = 19.53         # Abstand der Rädermittelpunkte in cm

    def __init__(self):
        os.system('setfont Lat15-TerminusBold14')

        self._lMot = LargeMotor(OUTPUT_B)
        self._rMot = LargeMotor(OUTPUT_C)
        self._col_l = MyColorSensorEV3(INPUT_1, 6, 69)
        self._col_r = MyColorSensorEV3(INPUT_2, 4, 54)
        self._btn = Button()

        self._lMot.reset()
        self._rMot.reset()
        self._lMot.polarity = "inversed"
        self._rMot.polarity = "inversed"

        print("press button to start")
        self.wait_until_button()

    def wait_until_button(self):
        while not self._btn.any():  # While no button is pressed.
            time.sleep(0.01)  # Wait 0.01 second

    def reset(self):
        self._lMot.reset()
        self._rMot.reset()

    @staticmethod
    def _steering(direction, speed):
        if direction >= 0:
            speed_left = speed
            speed_right = (100 - direction)/100 * speed
        else:
            speed_right = speed
            speed_left = (100 + direction)/100 * speed

        speed_left = max(-100, min(speed_left, 100))
        speed_right = max(-100, min(speed_right, 100))
        return int(speed_left), int(speed_right)

    @staticmethod
    def _min_speed(speed, min_speed=20):
        min_speed = abs(min_speed)
        if abs(speed) < min_speed:
            if speed > 0:
                speed = min_speed
            elif speed < 0:
                speed = -min_speed
        return speed

    def _cm_to_deg(self, cm):
        return 360 * cm / (math.pi * self._tyre_size)

    def drive(self, speed_start, speed, distance, direction=0, brake_action="run", kp=1, ki=0.05, kd=0.5):
        self._rMot.position = 0
        self._lMot.position = 0
        driven_distance = 0
        distance = self._cm_to_deg(distance)

        direction = max(-100, min(direction, 100))
        if speed_start is 0:
            speed_start = math.copysign(5, speed)

        k_left_mot = k_right_mot = 1
        if direction >= 0:
            k_left_mot = 1 - direction/100
        else:
            k_right_mot = 1 + direction/100

        last_error = integral = 0

        self._rMot.run_direct()
        self._lMot.run_direct()

        while driven_distance <= distance:
            driven_distance = (abs(self._rMot.position) + abs(self._lMot.position)) / 2

            error = self._rMot.position * k_right_mot - self._lMot.position * k_left_mot
            integral = float(0.5) * integral + error
            derivative = error - last_error
            last_error = error
            correction = error * kp + ki * integral + kd * derivative
            if speed < 0 or speed_start < 0:
                correction = -correction

            speed_accelerated = self._min_speed(speed_start + driven_distance / distance * (speed - speed_start))

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._steering(direction + correction, speed_accelerated)):
                motor.duty_cycle_sp = power

        if brake_action is not "run":
            self.brake(brake_action)

    def brake(self, action="hold"):
        self._lMot.stop(stop_action=action)
        self._rMot.stop(stop_action=action)

    def pivot(self, direction, forward=True):
        distance_degree = self._cm_to_deg(math.pi / 180 * abs(direction) * self._motor_distance)
        if not forward:
            distance_degree *= -1
        if direction < 0:
            self._lMot.stop(stop_action="hold")
            self._rMot.run_to_rel_pos(speed_sp=1000, position_sp=distance_degree, ramp_up_sp=1500,
                                      ramp_down_sp=1500, stop_action="hold")
            self._rMot.wait_while("running")
        else:
            self._rMot.stop(stop_action="hold")
            self._lMot.run_to_rel_pos(speed_sp=1000, position_sp=distance_degree, ramp_up_sp=1500,
                                      ramp_down_sp=1500, stop_action="hold")
            self._lMot.wait_while("running")

    def align(self):
        k_dir = -0.5
        k_speed = -0.5
        offset = 50
        tolerance = 3
        self._lMot.run_direct()
        self._rMot.run_direct()
        while not(offset - tolerance <= self._col_l.light_reflected() is self._col_r.light_reflected()
                  <= offset + tolerance):
            l_val = self._col_l.light_reflected()
            r_val = self._col_r.light_reflected()
            error_dir = k_dir*(r_val - l_val)
            error_dist = self._min_speed(k_speed*( offset - (r_val + l_val)/2))
            print("dir: " + str(error_dir) + "; dist: " + str(error_dist))

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._steering(error_dir, error_dist)):
                motor.duty_cycle_sp = power

            # error_left = offset - self._col_l.light_reflected()
            # error_right = offset - self._col_r.light_reflected()
            # self._lMot.duty_cycle_sp = self._min_speed(error_left * kp)
            # self._rMot.duty_cycle_sp = self._min_speed(error_right * kp)

# r._lMot.run_to_rel_pos(speed_sp=800, position_sp=3*360, ramp_up_sp=2000, stop_action="hold")
