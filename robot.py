from ev3dev.auto import *
import os
import math
from enum import Enum


class MyColorSensorEV3(ColorSensor):
    def __init__(self, port=INPUT_1, min_val=0, max_val=100):
        # self._col = ColorSensor(port)
        ColorSensor.__init__(self, port)
        self._min_val = min_val
        self._max_val = max_val
        self.mode = 'COL-REFLECT'
        # self._col.mode = 'COL-REFLECT'

    def light_reflected(self):
        # if self.mode is not 'COL-REFLECT':
        #    self.mode = 'COL-REFLECT'
        val = self.value()/(self._max_val-self._min_val) * 100
        val = min(100, val)
        val = max(0, val)
        return val


class MyColor(Enum):
    NOCOLOR = 0
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5


class MySlider(LargeMotor):
    def __init__(self, port=OUTPUT_A):
        LargeMotor.__init__(self, port)

    def open(self, wait=True, speed=100, duration=12):
        speed *= 10
        duration *= 100
        self.run_timed(time_sp=duration, speed_sp=speed, ramp_up_sp=800, ramp_down_sp=700)
        if wait:
            self.wait_while('running')

    def close(self, wait=True, speed=100, duration=13):
        speed *= -10
        duration *= 100
        self.run_timed(time_sp=duration, speed_sp=speed, ramp_up_sp=800, ramp_down_sp=700)
        if wait:
            self.wait_while('running')

    def collect(self):
        self.run_timed(time_sp=5000, speed_sp=-300, ramp_up_sp=800)
        self.wait_while('running')

    def open_slow(self):
        self.run_timed(time_sp=4000, speed_sp=300, ramp_up_sp=800)
        self.wait_while('running')

    def open_half_to_full(self, wait=True):
        self.open(wait, 100, 7)

    def open_to_half(self):
        self.run_to_rel_pos(position_sp=620, speed_sp=400, stop_action="hold")
        self.wait_while('running')


class MyLifter(MediumMotor):
    def __init__(self, port=OUTPUT_D):
        MediumMotor.__init__(self, port)
    # TODO: Implementation


class RobotConstants:
    tyre_size = 6.24                        # Durchmesser des Reifens in cm
    motor_distance = 19.6                   # Abstand der Rädermittelpunkte in cm
    sensor_distance = 14.5
    pivot_min_speed = 30
    drive_min_speed = 20


class Utils:
    def __init__(self, consts=RobotConstants()):
        self._consts = consts

    @staticmethod
    def steering(direction, speed):
        if direction >= 0:
            speed_left = speed
            speed_right = (100 - direction)/100 * speed
        else:
            speed_right = speed
            speed_left = (100 + direction)/100 * speed

        speed_left = max(-100, min(speed_left, 100))
        speed_right = max(-100, min(speed_right, 100))
        # print("l: " + str(speed_left) + "; r: " + str(speed_right))
        return int(speed_left), int(speed_right)

    def min_speed(self, speed, min_speed=0):
        if min_speed is 0:
            min_speed = self._consts.drive_min_speed

        min_speed = abs(min_speed)
        if abs(speed) < min_speed:
            if speed > 0:
                speed = min_speed
            elif speed < 0:
                speed = -min_speed
        return speed

    def midpoint_distance_from_line(self, direction):
        direction = math.radians(abs(direction))
        return math.sin(direction) * self._consts.sensor_distance/2

    def get_turn_correction_values(self, direction, parallel_distance):
        if direction is 0:
            return parallel_distance, 0

        r = parallel_distance / math.sin(math.radians(abs(direction)))
        average_distance = math.pi * r * abs(direction) / 180
        r1 = r + self._consts.motor_distance/2
        r2 = r - self._consts.motor_distance/2

        turn = 100 * r2/r1 - 100
        if direction < 0:
            turn *= -1

        return average_distance, turn

    def cm_to_deg(self, cm):
        return 360 * cm / (math.pi * self._consts.tyre_size)

    def deg_to_cm(self, deg):
        return deg * math.pi * self._consts.tyre_size / 360

    @staticmethod
    def pid(error, integral, last_error, kp, ki, kd):
        integral = integral + error
        derivative = error - last_error
        last_error = error
        correction = error * kp + ki * integral + kd * derivative
        return integral, last_error, correction

    @staticmethod
    def acceleration_speed_forward(driven_distance, distance, start_speed, max_speed, min_speed, k_acceleration):
        speed = k_acceleration * driven_distance + start_speed
        speed = min(speed, k_acceleration * (distance - driven_distance), max_speed)
        speed = max(speed, min_speed)
        return speed

    @staticmethod
    def steering_hard(direction, speed):                    # Deprecated

        s = (50 - abs(float(direction))) / 50

        speed_left = speed_right = speed
        if direction >= 0:
            speed_right *= s
            if direction > 100:
                speed_right = - speed
        else:
            speed_left *= s
            if direction < -100:
                speed_left = - speed

        speed_left = max(-100, min(speed_left, 100))
        speed_right = max(-100, min(speed_right, 100))
        return int(speed_left), int(speed_right)

    @staticmethod
    def distance_to_parallel_line(distance, direction=0):   # Deprecated
        direction = abs(direction)
        print("direction: " + str(direction))
        assert direction < 90
        print("distance " + str(distance / math.sin(math.radians(90 - direction))))
        return distance / math.sin(math.radians(90 - direction))


class Robot:
    container_colors = [MyColor.BLUE, MyColor.RED, MyColor.GREEN]

    def __init__(self):
        os.system('setfont Lat15-TerminusBold14')
        self._consts = RobotConstants()
        self._util = Utils(self._consts)

        self._lMot = LargeMotor(OUTPUT_B)
        self._rMot = LargeMotor(OUTPUT_C)
        self.slider = MySlider(OUTPUT_A)
        self.lifter = MyLifter(OUTPUT_D)

        # TODO: Add connectivity check

        self._col_l = MyColorSensorEV3(INPUT_1, 7, 73)
        self._col_r = MyColorSensorEV3(INPUT_2, 3, 51)
        self._btn = Button()

        self._lMot.reset()
        self._rMot.reset()
        self._lMot.polarity = "inversed"
        self._rMot.polarity = "inversed"

        print("press button to start")
        # self.wait_until_button()

    def wait_until_button(self):
        while not self._btn.any():  # While no button is pressed.
            time.sleep(0.01)  # Wait 0.01 second

    @staticmethod
    def speak(text, wait=True):
        if wait:
            Sound.speak(text).wait()
        else:
            Sound.speak(text)

    @staticmethod
    def beep(wait=False):
        if wait:
            Sound.beep().wait()
        else:
            Sound.beep()

    def reset(self):
        self._lMot.reset()
        self._rMot.reset()
        self.slider.reset()
        self.lifter.reset()

    def drive(self, speed_start, speed, distance, direction=0, brake_action="run", l_col_trigger=-1, r_col_trigger=-1,
              kp=8, ki=0.1, kd=1):
        # TODO: add time trigger

        difference = self._rMot.position - self._lMot.position
        self._rMot.position = 0
        self._lMot.position = -difference
        print("dif: " + str(difference))

        driven_distance = 0
        distance = self._util.cm_to_deg(distance)

        min_speed = self._consts.drive_min_speed
        if speed_start is 0:
            speed_start = math.copysign(min_speed, speed)

        k_left_mot = k_right_mot = 1
        if direction >= 0:
            k_left_mot = 1 - direction/100
        else:
            k_right_mot = 1 + direction/100

        last_error = integral = 0

        self._rMot.run_direct()
        self._lMot.run_direct()

        while driven_distance < distance and \
                self._col_l.light_reflected() > l_col_trigger and self._col_r.light_reflected() > r_col_trigger:

            driven_distance = (abs(self._rMot.position) + abs(self._lMot.position)) / 2

            error = self._rMot.position * k_right_mot - self._lMot.position * k_left_mot
            integral, last_error, correction = self._util.pid(error, integral, last_error, kp, ki, kd)

            if speed < 0 or speed_start < 0:
                correction = -correction

            speed_accelerated = self._util.min_speed(speed_start + driven_distance / distance * (speed - speed_start),
                                                     min_speed)

            # TODO: revise stall detection
            if direction <= 0 and self._lMot.is_stalled:
                self.beep()
                min_speed += 5
            if direction >= 0 and self._rMot.is_stalled:
                self.beep()
                min_speed += 5

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._util.steering(direction + correction, speed_accelerated)):
                motor.duty_cycle_sp = power
        self.brake(brake_action)

        # TODO: calculate difference in curve driving
        if direction is not 0:
            self.reset_motor_pos()

    def drive_triple(self,
                     speed_start, speed_max, speed_end,
                     distance_acceleration, distance_middle, distance_deceleration,
                     direction=0, brake_action="run",
                     l_col_trigger=-1, r_col_trigger=-1,
                     kp=1, ki=0.05, kd=0.5):
        self.drive(speed_start, speed_max, distance_acceleration, direction, "run",
                   l_col_trigger, r_col_trigger, kp, ki, kd)
        self.drive(speed_max, speed_max, distance_middle, direction, "run", l_col_trigger, r_col_trigger, kp, ki, kd)
        self.drive(speed_max, speed_end, distance_deceleration, direction, brake_action,
                   l_col_trigger, r_col_trigger, kp, ki, kd)

    def brake(self, action="hold"):
        if action is not "run":
            self._lMot.stop(stop_action=action)
            self._rMot.stop(stop_action=action)

    # TODO: Implement Turning

    def pivot(self, direction, forward=True, start_speed=0, min_speed=0, max_speed=80, k_acceleration=0.7):
        distance_degree = self._util.cm_to_deg(math.pi / 180 * abs(direction) * self._consts.motor_distance)
        driven_distance = self._rMot.position = self._lMot.position = 0

        start_speed = abs(start_speed)
        min_speed = abs(min_speed)
        max_speed = abs(max_speed)

        if min_speed is 0:
            min_speed = self._consts.pivot_min_speed

        if direction < 0:
            self._lMot.stop(stop_action="hold")
            self._rMot.run_direct()
            while driven_distance < distance_degree:
                driven_distance = abs(self._rMot.position)
                speed = self._util.acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed,
                                                              min_speed, k_acceleration)
                if not forward:
                    speed *= -1
                self._rMot.duty_cycle_sp = speed

                if self._rMot.is_stalled:
                    self.beep()
                    min_speed += 5
            self._rMot.stop(stop_action="hold")
        else:
            self._rMot.stop(stop_action="hold")
            self._lMot.run_direct()
            while driven_distance < distance_degree:
                driven_distance = abs(self._lMot.position)
                speed = self._util.acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed,
                                                              min_speed, k_acceleration)
                if not forward:
                    speed *= -1
                self._lMot.duty_cycle_sp = speed

                if self._lMot.is_stalled:
                    self.beep()
                    min_speed += 5
            self._lMot.stop(stop_action="hold")

        self.reset_motor_pos()

    def align_driving(self, speed=60, end_speed=40, distance_constant=2.5, distance_deceleration=5, brake_action="run"):
        end_speed = math.copysign(end_speed, speed)
        distance_constant = abs(distance_constant)
        distance_deceleration = abs(distance_deceleration)
        distance_from_line = distance_constant + distance_deceleration

        direction = self.get_direction(speed)       # Calculate error

        if speed < 0:
            direction *= -1

        if self._util.midpoint_distance_from_line(direction) > distance_from_line:
            self.speak("distance to short", False)
            # TODO: Turn on spot
        else:
            distance, turn = self._util.get_turn_correction_values(
                direction, distance_from_line - self._util.midpoint_distance_from_line(direction))

            if distance < distance_deceleration:
                self.drive(speed, end_speed, distance, turn, brake_action)
            else:
                self.drive(speed, speed, distance - distance_deceleration, turn)
                self.drive(speed, end_speed, distance_deceleration, turn, brake_action)

    def reset_motor_pos(self):
        self._lMot.position = 0
        self._rMot.position = 0

    def align(self, k_dir=1, offset=50, tolerance=0):
        k_dir *= -0.5
        self._lMot.run_direct()
        self._rMot.run_direct()
        while not(
                offset - tolerance <= self._col_l.light_reflected() is self._col_r.light_reflected()
                <= offset + tolerance
                or (self._lMot.is_stalled and self._rMot.is_stalled)):

            error_left = offset - self._col_l.light_reflected()
            error_right = offset - self._col_r.light_reflected()
            self._lMot.duty_cycle_sp = error_left * k_dir
            self._rMot.duty_cycle_sp = error_right * k_dir
        self.brake()

    def get_direction(self, speed, brake_action="run", kp=1, ki=0.05, kd=0.5):
        self._rMot.position = self._lMot.position = 0
        l_distance = r_distance = 0
        l_triggered = r_triggered = False
        trigger_value = 50

        last_error = integral = 0

        self._rMot.run_direct()
        self._lMot.run_direct()

        while not (l_triggered and r_triggered):
            driven_distance = (abs(self._rMot.position) + abs(self._lMot.position)) / 2

            if self._col_l.light_reflected() < trigger_value and not l_triggered:
                l_triggered = True
                l_distance = driven_distance
            if self._col_r.light_reflected() < trigger_value and not r_triggered:
                r_triggered = True
                r_distance = driven_distance

            error = self._rMot.position - self._lMot.position
            integral, last_error, correction = self._util.pid(error, integral, last_error, kp, ki, kd)

            if speed < 0:
                correction = -correction

            for (motor, power) in zip((self._lMot, self._rMot), self._util.steering(correction, speed)):
                motor.duty_cycle_sp = power

        self.brake(brake_action)

        s = abs(r_distance - l_distance)
        print("ANGLE: s = " + str(s))
        if s <= 0:
            direction = 0
        else:
            direction = 90-math.degrees(math.atan(self._util.cm_to_deg(self._consts.sensor_distance / s)))
            if not l_distance < r_distance:
                direction *= -1
            if speed < 0:
                direction *= -1
        print("measured angle: " + str(direction))
        return direction
