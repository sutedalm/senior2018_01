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
    _sensor_distance = 14.5

    def __init__(self):
        os.system('setfont Lat15-TerminusBold14')

        self._lMot = LargeMotor(OUTPUT_B)
        self._rMot = LargeMotor(OUTPUT_C)
        self._col_l = MyColorSensorEV3(INPUT_1, 7, 81)
        self._col_r = MyColorSensorEV3(INPUT_2, 4, 56)
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
    def _steering_hard(direction, speed):

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
    def _min_speed(speed, min_speed=20):
        min_speed = abs(min_speed)
        if abs(speed) < min_speed:
            if speed > 0:
                speed = min_speed
            elif speed < 0:
                speed = -min_speed
        return speed

    @staticmethod
    def distance_to_parallel_line(distance, direction=0):
        direction = abs(direction)
        print("direction: " + str(direction))
        assert direction < 90
        print("distance " + str(distance / math.sin(math.radians(90 - direction))))
        return distance / math.sin(math.radians(90 - direction))

    def midpoint_distance_from_line(self, direction):
        direction = math.radians(abs(direction))
        return math.sin(direction) * self._sensor_distance/2

    def get_turn_correction_values(self, direction, parallel_distance):
        if direction is 0:
            return parallel_distance, 0

        r = parallel_distance / math.sin(math.radians(abs(direction)))
        average_distance = math.pi * r * abs(direction) / 180
        r1 = r + self._motor_distance/2
        r2 = r - self._motor_distance/2
        if direction > 0:
            turn = 100 - 100 * r1/r2
        else:
            turn = 100 * r1/r2 - 100
        return average_distance, turn

    def _cm_to_deg(self, cm):
        return 360 * cm / (math.pi * self._tyre_size)

    def drive(self, speed_start, speed, distance, direction=0, brake_action="run", kp=1, ki=0.05, kd=0.5):
        self._rMot.position = 0
        self._lMot.position = 0
        driven_distance = 0
        distance = self._cm_to_deg(distance)

        # direction = max(-100, min(direction, 100))
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
        self.brake(brake_action)

    def move_to_line(self, speed, l_trigger_value=50, r_trigger_value=50, brake_action="run", kp=1, ki=0.05, kd=0.5):
        self._rMot.position = self._lMot.position = 0

        last_error = integral = 0

        self._rMot.run_direct()
        self._lMot.run_direct()

        while not(self._col_l.light_reflected() < l_trigger_value or self._col_r.light_reflected() < r_trigger_value):
            error = self._rMot.position - self._lMot.position
            integral = float(0.5) * integral + error
            derivative = error - last_error
            last_error = error
            correction = error * kp + ki * integral + kd * derivative
            if speed < 0:
                correction = -correction

            for (motor, power) in zip((self._lMot, self._rMot), self._steering(correction, speed)):
                motor.duty_cycle_sp = power
        self.brake(brake_action)

    def brake(self, action="hold"):
        if action is not "run":
            self._lMot.stop(stop_action=action)
            self._rMot.stop(stop_action=action)

    @staticmethod
    def _acceleration_speed_forward(driven_distance, distance, start_speed, max_speed, min_speed, k_acceleration):
        speed = k_acceleration * driven_distance + start_speed
        speed = min(speed, k_acceleration * (distance - driven_distance), max_speed)
        speed = max(speed, min_speed)
        return speed

    def pivot(self, direction, forward=True, start_speed=0, max_speed=100, k_acceleration=0.7):
        distance_degree = self._cm_to_deg(math.pi / 180 * abs(direction) * self._motor_distance)
        driven_distance = self._rMot.position = self._lMot.position = 0
        start_speed = abs(start_speed)
        if direction < 0:
            self._lMot.stop(stop_action="hold")
            self._rMot.run_direct()
            while driven_distance < distance_degree:
                driven_distance = abs(self._rMot.position)
                speed = self._acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed, 20,
                                                         k_acceleration)
                if not forward:
                    speed *= -1
                self._rMot.duty_cycle_sp = speed
            self._rMot.stop(stop_action="hold")
        else:
            self._rMot.stop(stop_action="hold")
            self._lMot.run_direct()
            while driven_distance < distance_degree:
                driven_distance = abs(self._lMot.position)
                speed = self._acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed, 20,
                                                         k_acceleration)
                if not forward:
                    speed *= -1
                self._lMot.duty_cycle_sp = speed
            self._lMot.stop(stop_action="hold")

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
        self._rMot.position = 0
        self._lMot.position = 0
        start_distance = 0
        l_triggered = r_triggered = finished = False
        left_first = True
        trigger_value = 50

        last_error = integral = 0

        self._rMot.run_direct()
        self._lMot.run_direct()

        while not finished:
            driven_distance = (abs(self._rMot.position) + abs(self._lMot.position)) / 2

            if self._col_l.light_reflected() < trigger_value:
                l_triggered = True
            if self._col_r.light_reflected() < trigger_value:
                r_triggered = True

            if l_triggered and r_triggered:
                finished = True
            elif (l_triggered ^ r_triggered) and start_distance is 0:   # XOR
                start_distance = driven_distance
                left_first = l_triggered

            error = self._rMot.position - self._lMot.position
            integral = float(0.5) * integral + error
            derivative = error - last_error
            last_error = error
            correction = error * kp + ki * integral + kd * derivative
            if speed < 0:
                correction = -correction

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._steering(correction, speed)):
                motor.duty_cycle_sp = power

        self.brake(brake_action)

        s = driven_distance - start_distance
        if s is 0:
            return 0
        direction = 90-math.degrees(math.atan(self._cm_to_deg(self._sensor_distance / s)))
        if not left_first:
            direction *= -1
        if speed < 0:
            direction *= -1
        return direction


# r._lMot.run_to_rel_pos(speed_sp=800, position_sp=3*360, ramp_up_sp=2000, stop_action="hold")
