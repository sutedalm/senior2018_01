from ev3dev.auto import *
import os
import math
from enum import IntEnum


class MyColorSensorEV3(ColorSensor):
    def __init__(self, port=INPUT_1, min_val=0, max_val=100):
        ColorSensor.__init__(self, port)
        assert self.connected
        self._min_val = min_val
        self._max_val = max_val
        self.mode = 'COL-REFLECT'
        self.inversed = False

    def light_reflected(self):
        # MODE HAS TO BE SET TO 'COL-REFLECT' !!!

        value = self.value()
        self._min_val = min(self._min_val, value)
        self._max_val = max(self._max_val, value)

        val = value/(self._max_val-self._min_val) * 100
        val = min(100, val)
        val = max(0, val)

        if self.inversed:
            val = 100 - val

        return val

    def set_inversed(self, inversed=True):
        self.inversed = inversed


class MyColorSensorHT(Sensor):
    def __init__(self, port=INPUT_3, min_val=0, max_val=100):
        Sensor.__init__(self, port)
        assert self.connected

        self._min_val = min_val
        self._max_val = max_val
        self.mode = 'ALL'

    def get_color(self, iterations=10):
        if self.mode is not 'COLOR':
            self.mode = 'COLOR'

        for i in range(0, iterations):
            col = self.value()
            if col in {2, 3}:
                return MyColor.BLUE
            if col in {4, 13}:
                return MyColor.GREEN
            if col in {5, 6}:
                return MyColor.YELLOW
            if col in {7, 8, 9, 10}:
                return MyColor.RED
        if col is 0:
            return MyColor.NOCOLOR
        return MyColor.ERROR

    def light_reflected(self):
        if self.mode is not 'WHITE':
            self.mode = 'WHITE'

        value = self.value()
        self._min_val = min(self._min_val, value)
        self._max_val = max(self._max_val, value)

        val = value/(self._max_val-self._min_val) * 100
        val = min(100, val)
        val = max(0, val)
        return val


class MyColor(IntEnum):
    ERROR = -1
    NOCOLOR = 0
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5

    def to_text(self):
        return self.name


class MySlider(LargeMotor):
    def __init__(self, port=OUTPUT_A):
        LargeMotor.__init__(self, port)
        assert self.connected
        self.reset()

    def open(self, wait=True, speed=100, duration=13):
        speed *= 10
        duration *= 100
        self.run_timed(time_sp=duration, speed_sp=speed, ramp_up_sp=800, ramp_down_sp=700)
        if wait:
            self.wait_while('running')
            self.run_forever(speed_sp=200)

    def close(self, wait=True, speed=100, duration=13):
        speed *= -10
        duration *= 100
        self.run_timed(time_sp=duration, speed_sp=speed, ramp_up_sp=800, ramp_down_sp=700)
        if wait:
            self.wait_while('running')

    def hold_closed(self):
        self.run_direct(duty_cycle_sp=-40)

    def collect(self, wait=True):
        self.run_timed(time_sp=2000, speed_sp=-700, ramp_down_sp=1000)
        if wait:
            self.wait_while('running')
            self.hold_closed()

    def open_half_to_full(self, wait=True):
        self.open(wait, 100, 9)

    def open_to_half(self):
        self.run_to_rel_pos(position_sp=620, speed_sp=800, stop_action="brake")
        self.wait_while('running')

    def open_for_lifter(self, wait=True):
        self.run_to_rel_pos(position_sp=260, speed_sp=1000, stop_action="brake")
        if wait:
            self.wait_while('running')

    def open_for_ships(self, wait=True):
        self.run_to_rel_pos(position_sp=230, speed_sp=1000, stop_action="brake")
        if wait:
            self.wait_while('running')

    def open_for_base(self, wait=True):
        self.run_to_rel_pos(position_sp=190, speed_sp=1000, stop_action="brake")
        if wait:
            self.wait_while('running')


class MyLifterPosition(IntEnum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    TOP = 4


class MyLifter(MediumMotor):
    position_difference = 270

    def __init__(self, port=OUTPUT_D):
        MediumMotor.__init__(self, port)
        assert self.connected
        self.reset()
        self.lifter_position = MyLifterPosition.FIRST

    def move_up(self, wait=True):
        self.run_to_abs_pos(position_sp=self.position - self.position_difference, speed_sp=230,
                            ramp_up_sp=1000, ramp_down_sp=1000, stop_action='hold')
        if wait:
            self.wait_while('running')
        self.lifter_position += 1

    def move_down(self, wait=True):
        self.run_to_abs_pos(position_sp=self.position + self.position_difference, speed_sp=200, stop_action='hold')
        if wait:
            self.wait_while('running')
        self.lifter_position -= 1

    def move_to_first_position(self, wait=True):
        self.run_to_abs_pos(position_sp=0, speed_sp=1000, stop_action='hold')
        if wait:
            self.wait_while('running')

    def move_to_top_position(self, wait=True):
        self.run_to_abs_pos(position_sp=-3*self.position_difference, speed_sp=1000, stop_action='hold')
        if wait:
            self.wait_while('running')


class MyDrivingMotor(LargeMotor):
    def __init__(self, port=OUTPUT_B):
        LargeMotor.__init__(self, port)
        assert self.connected
        self.reset()
        self.polarity = "inversed"

    def init_reset(self):
        self.reset()
        self.polarity = "inversed"


class RobotConstants:
    tyre_size = 6.24                        # Durchmesser des Reifens in cm
    motor_distance = 19.38                  # Abstand der Rädermittelpunkte in cm
    motor_distance_turn = 19.75
    sensor_distance = 14.5
    pivot_min_speed = 30
    drive_min_speed = 50
    col_trigger_val = 50

    drive_kp = 5
    drive_ki = 0.02
    drive_kd = 2

    turn_kp = 1
    turn_ki = 0
    turn_kd = 0.5

    lflw_kp = 1
    lflw_ki = 0
    lflw_kd = 1


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
        r1 = r + self._consts.motor_distance_turn/2
        r2 = r - self._consts.motor_distance_turn/2

        turn = 100 * r2/r1 - 100
        if direction < 0:
            turn *= -1

        return average_distance, turn

    def cm_to_deg(self, cm):
        return 360 * cm / (math.pi * self._consts.tyre_size)

    def deg_to_cm(self, deg):
        return deg * math.pi * self._consts.tyre_size / 360

    @staticmethod
    def clamp_speed(speed, minimum=-100, maximum=100):
        return max(minimum, min(maximum, speed))

    @staticmethod
    def pid(error, integral, last_error, kp, ki, kd):
        integral = integral + error
        derivative = error - last_error
        last_error = error
        correction = error * kp + ki * integral + kd * derivative
        return integral, last_error, correction

    @staticmethod
    def acceleration_speed_forward(driven_distance, distance, start_speed, max_speed, min_speed,
                                   k_acceleration, k_deceleration=6):
        driven_distance = abs(driven_distance)
        distance = abs(distance)
        speed = k_acceleration * math.sqrt(max(0, driven_distance)) + start_speed
        speed = min(speed, k_deceleration * math.sqrt(max(0, distance - driven_distance)), max_speed)
        speed = max(speed, min_speed)
        return speed

    @staticmethod
    def distance_reached(driven_distance, distance, start_speed):
        distance = abs(distance)
        if start_speed < 0 and driven_distance <= -distance:
            return True
        if start_speed >= 0 and driven_distance >= distance:
            return True
        return False

    @staticmethod
    def distance_reached_bool(driven_distance, distance, forward=True):
        distance = abs(distance)
        if not forward and driven_distance <= -distance:
            return True
        if forward and driven_distance >= distance:
            return True
        return False

    @staticmethod
    def distance_to_parallel_line(distance, direction=0):
        direction = abs(direction)
        # print("direction: " + str(direction))
        assert direction < 90
        # print("distance " + str(distance / math.sin(math.radians(90 - direction))))
        return distance / math.sin(math.radians(90 - direction))

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


class Robot:
    def __init__(self):
        os.system('setfont Lat15-TerminusBold14')
        self.consts = RobotConstants()
        self._util = Utils(self.consts)

        self._lMot = MyDrivingMotor(OUTPUT_B)
        self._rMot = MyDrivingMotor(OUTPUT_C)
        self.slider = MySlider(OUTPUT_A)
        self.lifter = MyLifter(OUTPUT_D)

        self.col_l = MyColorSensorEV3(INPUT_1, 8, 75)
        self.col_r = MyColorSensorEV3(INPUT_2, 3, 45)
        self.ht_middle = MyColorSensorHT(INPUT_3, 0, 30)
        # self.col_l = MyColorSensorEV3(INPUT_1, 7, 85)
        # self.col_r = MyColorSensorEV3(INPUT_2, 4, 58)
        # self.ht_middle = MyColorSensorHT(INPUT_3, 0, 25)
        self.ht_side = MyColorSensorHT(INPUT_4)

        self._btn = Button()

        self.container_colors = [MyColor.BLUE, MyColor.GREEN, MyColor.YELLOW]

        print("press button to start")
        # self.wait_until_button()

    def wait_until_button(self):
        while not self._btn.any():
            time.sleep(0.01)

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
        self._lMot.init_reset()
        self._rMot.init_reset()
        self.slider.reset()
        self.lifter.reset()

    def drive(self, speed_start, speed, distance, direction=0, brake_action="run", l_col_trigger=-1, r_col_trigger=-1,
              kp=RobotConstants.drive_kp, ki=RobotConstants.drive_ki, kd=RobotConstants.drive_kd):

        # TODO: add time trigger
        # print("DRIVING")

        driven_distance = 0
        distance = abs(self._util.cm_to_deg(distance))
        # print("distance: " + str(distance))

        min_speed = self.consts.drive_min_speed
        if speed_start is 0:
            speed_start = math.copysign(min_speed, speed)

        k_left_mot = k_right_mot = 1
        if direction >= 0:
            k_left_mot = 1 - direction/100
        else:
            k_right_mot = 1 + direction/100

        last_error = integral = 0

        line_detected = False

        self._rMot.run_direct()
        self._lMot.run_direct()

        while not self._util.distance_reached(driven_distance, distance, speed_start) and not line_detected:
            line_detected = self.col_l.light_reflected() <= l_col_trigger or \
                            self.col_r.light_reflected() <= r_col_trigger

            l_pos = self._lMot.position
            r_pos = self._rMot.position
            r_pos = (self._rMot.position+r_pos)/2
            l_pos = (self._lMot.position+l_pos)/2

            driven_distance = (r_pos + l_pos) / 2
            if self._util.distance_reached(driven_distance, distance, speed_start) or line_detected:
                # only for faster brake response time
                break

            error = r_pos * k_right_mot - l_pos * k_left_mot
            integral, last_error, correction = self._util.pid(error, integral, last_error, kp, ki, kd)

            if speed < 0 or speed_start < 0:
                correction = -correction

            speed_accelerated = self._util.min_speed(speed_start + abs(driven_distance) /
                                                     distance * (speed - speed_start), min_speed)

            if direction <= 0 and self._lMot.is_stalled:
                self.beep()
                min_speed += 2
            if direction >= 0 and self._rMot.is_stalled:
                self.beep()
                min_speed += 2

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._util.steering(direction + correction, speed_accelerated)):
                motor.duty_cycle_sp = power
            # print("l_pos: " + str(self._lMot.position) + "; r_pos: " + str(self._rMot.position))

        # print("end_l_pos: " + str(l_pos) + "; end_r_pos: " + str(r_pos))
        if not line_detected:
            distance = math.copysign(distance, speed_start)
            if direction >= 0:
                k = (100 - direction)/100
                distance_l = distance * 2/(1+k)
                distance_r = distance * 2/(1+k) * k
            else:
                k = (100 + direction)/100
                distance_r = distance * 2/(1+k)
                distance_l = distance * 2/(1+k) * k

            self._rMot.position = self._rMot.position - distance_r
            self._lMot.position = self._lMot.position - distance_l
        else:
            print("LINE DETECTED")
            self.reset_motor_pos()
        # print("newl: " + str(self._lMot.position) + "; newr: " + str(self._rMot.position))
        self.brake(brake_action)
        return line_detected

    def drive_color(self, speed_start, speed, distance, direction=0, brake_action="run",
                    l_col_trigger=False, r_col_trigger=False,
                    kp=RobotConstants.drive_kp, ki=RobotConstants.drive_ki, kd=RobotConstants.drive_kd):

        # TODO: add time trigger
        # print("DRIVING")
        self.col_r.mode = 'COL-COLOR'
        self.col_l.mode = 'COL-COLOR'

        driven_distance = 0
        distance = abs(self._util.cm_to_deg(distance))
        # print("distance: " + str(distance))

        min_speed = self.consts.drive_min_speed
        if speed_start is 0:
            speed_start = math.copysign(min_speed, speed)

        k_left_mot = k_right_mot = 1
        if direction >= 0:
            k_left_mot = 1 - direction/100
        else:
            k_right_mot = 1 + direction/100

        last_error = integral = 0

        line_detected = False

        self._rMot.run_direct()
        self._lMot.run_direct()

        while not self._util.distance_reached(driven_distance, distance, speed_start) and not line_detected:
            line_detected = (self.col_l.value() is 1 and l_col_trigger) or \
                            (self.col_r.value() is 1 and r_col_trigger)

            l_pos = self._lMot.position
            r_pos = self._rMot.position

            driven_distance = (r_pos + l_pos) / 2
            if self._util.distance_reached(driven_distance, distance, speed_start) or line_detected:
                # only for faster brake response time
                break

            error = r_pos * k_right_mot - l_pos * k_left_mot
            integral, last_error, correction = self._util.pid(error, integral, last_error, kp, ki, kd)

            if speed < 0 or speed_start < 0:
                correction = -correction

            speed_accelerated = self._util.min_speed(speed_start + abs(driven_distance) /
                                                     distance * (speed - speed_start), min_speed)

            if direction <= 0 and self._lMot.is_stalled:
                self.beep()
                min_speed += 2
            if direction >= 0 and self._rMot.is_stalled:
                self.beep()
                min_speed += 2

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._util.steering(direction + correction, speed_accelerated)):
                motor.duty_cycle_sp = power
            # print("l_pos: " + str(self._lMot.position) + "; r_pos: " + str(self._rMot.position))

        # print("end_l_pos: " + str(l_pos) + "; end_r_pos: " + str(r_pos))
        if not line_detected:
            distance = math.copysign(distance, speed_start)
            if direction >= 0:
                k = (100 - direction)/100
                distance_l = distance * 2/(1+k)
                distance_r = distance * 2/(1+k) * k
            else:
                k = (100 + direction)/100
                distance_r = distance * 2/(1+k)
                distance_l = distance * 2/(1+k) * k

            self._rMot.position = self._rMot.position - distance_r
            self._lMot.position = self._lMot.position - distance_l
        else:
            # print("LINE DETECTED")
            dif = self._rMot.position - self._lMot.position
            self.reset_motor_pos(dif)
        # print("newl: " + str(self._lMot.position) + "; newr: " + str(self._rMot.position))
        self.brake(brake_action)
        return line_detected

    def drive_triple(self,
                     speed_start, speed_max, speed_end,
                     distance_acceleration, distance_middle, distance_deceleration,
                     direction=0, brake_action="run",
                     l_col_trigger=-1, r_col_trigger=-1,
                     kp=RobotConstants. drive_kp, ki=RobotConstants.drive_ki, kd=RobotConstants.drive_kd):
        line_detected = False
        if not line_detected:
            line_detected = self.drive(speed_start, speed_max, distance_acceleration, direction, "run",
                                       l_col_trigger, r_col_trigger, kp, ki, kd)
        if not line_detected:
            line_detected = self.drive(speed_max, speed_max, distance_middle, direction, "run",
                                       l_col_trigger, r_col_trigger, kp, ki, kd)
        if not line_detected:
            line_detected = self.drive(speed_max, speed_end, distance_deceleration, direction, brake_action,
                                       l_col_trigger, r_col_trigger, kp, ki, kd)
        return line_detected

    def brake(self, action="brake"):
        if action is not "run":
            self._lMot.stop(stop_action=action)
            self._rMot.stop(stop_action=action)

    def turn(self, direction, start_speed=40, end_speed=40, max_speed=100, k_acceleration=5, k_deceleration=5,
             kp=RobotConstants.turn_kp, ki=RobotConstants.turn_ki, kd=RobotConstants.turn_kd):
        print("TURNING")
        print("dir: " + str(direction))
        distance_degree = self._util.cm_to_deg(math.pi / 180 * abs(direction) * self.consts.motor_distance_turn)
        driven_distance = 0

        end_speed = abs(end_speed)
        max_speed = abs(max_speed)

        last_error = integral = 0

        self._lMot.duty_cycle_sp = self._rMot.duty_cycle_sp = 0
        self._lMot.run_direct()
        self._rMot.run_direct()

        while not self._util.distance_reached_bool(driven_distance, distance_degree, True):
            l_pos = self._lMot.position
            r_pos = self._rMot.position

            driven_distance = abs(l_pos) + abs(r_pos)
            speed = self._util.acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed,
                                                          end_speed, k_acceleration, k_deceleration)

            error = abs(l_pos) - abs(r_pos)
            if direction < 0:
                error *= -1
            integral, last_error, correction = self._util.pid(error, integral, last_error, kp, ki, kd)

            if direction < 0:
                speed *= -1

            self._rMot.duty_cycle_sp = self._util.clamp_speed(-speed - correction)
            self._lMot.duty_cycle_sp = self._util.clamp_speed(speed - correction)

            if self._rMot.is_stalled or self._lMot.is_stalled:
                self.beep()
                end_speed += 5

        self._lMot.stop(stop_action="brake")
        self._rMot.stop(stop_action="brake")

        if direction > 0:
            distance_degree *= -1

        self._rMot.position -= distance_degree / 2
        self._lMot.position += distance_degree / 2

    def pivot(self, direction, forward=True, start_speed=0, min_speed=0, max_speed=100, k_acceleration=13):
        # print("PIVOTING")
        distance_degree = self._util.cm_to_deg(math.pi / 180 * abs(direction) * self.consts.motor_distance)
        driven_distance = 0

        # calculate previous error
        error = self._lMot.position - self._rMot.position
        l_pos = r_pos = 0
        if direction >= 0:
            l_pos = error
        else:
            r_pos = -error
        if not forward:
            l_pos *= -1
            r_pos *= -1
        self._lMot.position = l_pos
        self._rMot.position = r_pos

        start_speed = abs(start_speed)
        min_speed = abs(min_speed)
        max_speed = abs(max_speed)

        if min_speed is 0:
            min_speed = self.consts.pivot_min_speed

        if direction < 0:
            self._lMot.stop(stop_action="hold")
            self._rMot.run_direct()
            while not self._util.distance_reached_bool(driven_distance, distance_degree, forward):
                driven_distance = self._rMot.position
                speed = self._util.acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed,
                                                              min_speed, k_acceleration, k_acceleration)
                if not forward:
                    speed *= -1
                self._rMot.duty_cycle_sp = speed

                if self._rMot.is_stalled:
                    self.beep()
                    min_speed += 5

            self._lMot.stop(stop_action="brake")
            self._rMot.stop(stop_action="brake")
            self._lMot.position = 0
            if forward:
                self._rMot.position -= distance_degree
            else:
                self._rMot.position += distance_degree
        else:
            self._rMot.stop(stop_action="hold")
            self._lMot.run_direct()
            while not self._util.distance_reached_bool(driven_distance, distance_degree, forward):
                driven_distance = self._lMot.position
                speed = self._util.acceleration_speed_forward(driven_distance, distance_degree, start_speed, max_speed,
                                                              min_speed, k_acceleration)
                if not forward:
                    speed *= -1
                self._lMot.duty_cycle_sp = speed

                if self._lMot.is_stalled:
                    self.beep()
                    min_speed += 5

            self._rMot.stop(stop_action="brake")
            self._lMot.stop(stop_action="brake")
            self._rMot.position = 0
            if forward:
                self._lMot.position -= distance_degree
            else:
                self._lMot.position += distance_degree

    def align_driving(self, speed=60, end_speed=40, distance_constant=2.5, distance_deceleration=5, brake_action="run"):
        print("ALIGN DRIVING")
        end_speed = math.copysign(end_speed, speed)
        distance_constant = abs(distance_constant)
        distance_deceleration = abs(distance_deceleration)
        distance_from_line = distance_constant + distance_deceleration

        direction = self.get_direction(speed)       # Calculate error

        if speed < 0:
            direction *= -1

        if self._util.midpoint_distance_from_line(direction) > distance_from_line:
            print("distance to short")
            self.turn(-direction)
        else:
            distance, turn = self._util.get_turn_correction_values(
                direction, distance_from_line - self._util.midpoint_distance_from_line(direction))

            if distance < distance_deceleration:
                self.drive(speed, end_speed, distance, turn, brake_action)
            else:
                self.drive(speed, speed, distance - distance_deceleration, turn)
                self.drive(speed, end_speed, distance_deceleration, turn, brake_action)

    def reset_motor_pos(self, dif=0):
        if dif > 0:
            self._lMot.position = dif
            self._rMot.position = 0
        else:
            self._lMot.position = 0
            self._rMot.position = -dif

    def line_follow(self, speed_start, speed, distance=30, offset=50, brake_action="run",
                    side=False, l_col_trigger=False, r_col_trigger=False,
                    kp=RobotConstants.lflw_kp, ki=RobotConstants.lflw_ki, kd=RobotConstants.lflw_kd):
        # print("LINEFOLLOW")
        self.col_r.mode = 'COL-COLOR'
        self.col_l.mode = 'COL-COLOR'

        driven_distance = 0
        distance = abs(self._util.cm_to_deg(distance))
        # print("distance: " + str(distance))

        min_speed = self.consts.drive_min_speed
        if speed_start is 0:
            speed_start = math.copysign(min_speed, speed)

        last_error = integral = 0

        line_detected = False

        self._rMot.run_direct()
        self._lMot.run_direct()

        while not self._util.distance_reached_bool(driven_distance, distance, True) and not line_detected:
            line_detected = (self.col_l.value() is 1 and l_col_trigger) or \
                            (self.col_r.value() is 1 and r_col_trigger)

            l_pos = self._lMot.position
            r_pos = self._rMot.position

            driven_distance = (r_pos + l_pos) / 2
            if self._util.distance_reached_bool(driven_distance, distance, speed_start) or line_detected:
                # only for faster brake response time
                break

            error = offset - self.ht_middle.light_reflected()
            integral, last_error, correction = self._util.pid(error, integral, last_error, kp, ki, kd)

            if side is False:
                correction = -correction

            speed_accelerated = self._util.min_speed(speed_start + abs(driven_distance) /
                                                     distance * (speed - speed_start), min_speed)

            if self._lMot.is_stalled or self._rMot.is_stalled:
                self.beep()
                min_speed += 2

            for (motor, power) in zip((self._lMot, self._rMot),
                                      self._util.steering(correction, speed_accelerated)):
                motor.duty_cycle_sp = power
        self.reset_motor_pos()
        self.brake(brake_action)
        return line_detected

    def align_new(self, k_dir=1, offset=50, tolerance=0):
        # TODO: revise (add time trigger, check tolerance)
        k_dir *= 0.5
        k_move = 1
        self._lMot.run_direct()
        self._rMot.run_direct()

        integral = last_error_turn = last_error_drive = 0
        while not(
                offset - tolerance <= self.col_l.light_reflected() is self.col_r.light_reflected()
                <= offset + tolerance):
                # or (self._lMot.is_stalled and self._rMot.is_stalled)):
            l_val = self.col_l.light_reflected()
            r_val = self.col_r.light_reflected()
            error_turn = r_val - l_val
            error_move = (r_val + l_val)/2 - offset
            integral, last_error_turn, correction = self._util.pid(error_turn, integral, last_error_turn, k_dir, 0, 1)
            integral, last_error_drive, speed = self._util.pid(error_move, integral, last_error_drive, k_move, 0, 0)
            self._lMot.duty_cycle_sp = self._util.clamp_speed(speed - correction)
            self._rMot.duty_cycle_sp = self._util.clamp_speed(speed + correction)

            print("err: " + str(error_turn) + "; cor: " + str(correction))
        self.brake()
        self.reset_motor_pos()

    def align(self, k_dir=1, offset=50, tolerance=0):
        # TODO: revise (add time trigger, check tolerance)
        k_dir *= -0.7
        self._lMot.run_direct()
        self._rMot.run_direct()
        while not(
                offset - tolerance <= self.col_l.light_reflected() is self.col_r.light_reflected()
                <= offset + tolerance
                or (self._lMot.is_stalled and self._rMot.is_stalled)):

            error_left = offset - self.col_l.light_reflected()
            error_right = offset - self.col_r.light_reflected()
            speed_left = error_left * k_dir
            speed_right = error_right * k_dir
            self._lMot.duty_cycle_sp = self._util.clamp_speed(speed_left)
            self._rMot.duty_cycle_sp = self._util.clamp_speed(speed_right)

        self.brake()
        self.reset_motor_pos()

    def get_direction(self, speed, brake_action="run",
                      kp=RobotConstants.drive_kp, ki=RobotConstants.drive_ki, kd=RobotConstants.drive_kd,
                      max_direction=10):

        self._rMot.run_direct()
        self._lMot.run_direct()

        dif = self._lMot.position - self._rMot.position
        self.reset_motor_pos(dif)
        # print("l_pos: " + str(self._lMot.position) + "; r_pos: " + str(self._rMot.position))

        l_distance = r_distance = 0
        l_triggered = r_triggered = False
        trigger_value = self.consts.col_trigger_val

        last_error = integral = 0

        while not (l_triggered and r_triggered):
            driven_distance = (abs(self._rMot.position) + abs(self._lMot.position)) / 2
            l_col = self.col_l.light_reflected()
            r_col = self.col_r.light_reflected()

            if l_col < trigger_value and not l_triggered:
                l_triggered = True
                l_distance = driven_distance
            if r_col < trigger_value and not r_triggered:
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
        # print("ANGLE: s = " + str(s))
        if s <= 0:
            direction = 0
        else:
            direction = 90-math.degrees(math.atan(self._util.cm_to_deg(self.consts.sensor_distance / s)))
            if not l_distance < r_distance:
                direction *= -1
            if speed < 0:
                direction *= -1
        print("measured angle: " + str(direction))

        self.reset_motor_pos()
        return min(max_direction, max(-max_direction, direction))

    def get_direction_drive(self, speed=60, end_speed=40,
                            distance_constant=2.5, distance_deceleration=5, brake_action="run",
                            max_direction=10):
        print("GET_DIRECTION_DRIVE")

        direction = self.get_direction(speed, "run",
                                       RobotConstants.drive_kp, RobotConstants.drive_ki, RobotConstants.drive_kd,
                                       max_direction)

        end_speed = math.copysign(end_speed, speed)
        distance_constant = self._util.distance_to_parallel_line(abs(distance_constant), direction)
        distance_deceleration = self._util.distance_to_parallel_line(abs(distance_deceleration), direction)

        self.drive(speed, speed, distance_constant)
        self.drive(speed, end_speed, distance_deceleration, 0, brake_action)

        return direction
