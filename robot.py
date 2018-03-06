from ev3dev.auto import *
import os


class Robot:
    _lMot = LargeMotor(OUTPUT_B)
    _rMot = LargeMotor(OUTPUT_C)
    _btn = Button()

    def __init__(self):
        os.system('setfont Lat15-TerminusBold14')
        self._lMot.reset()
        self._rMot.reset()
        self._lMot.polarity = "inversed"
        self._rMot.polarity = "inversed"

        print("press button to start")
        while not self._btn.any():  # While no button is pressed.
            time.sleep(0.01)  # Wait 0.01 second

    def reset(self):
        self._lMot.reset()
        self._rMot.reset()

    @staticmethod
    def steering(direction, speed):
        if direction >= 0:
            speed_left = speed
            speed_right = (100 - direction)/100 * speed
        else:
            speed_right = speed
            speed_left = (100 + direction)/100 * speed
        return int(speed_left), int(speed_right)

    def drive(self, speed, dist, direction=0, kp=1, ki=0.05, kd=0.5):
        self._rMot.position = 0
        self._lMot.position = 0

        direction = max(-100, min(direction, 100))

        k_left_mot = k_right_mot = 1
        if direction >= 0:
            k_left_mot = 1 - direction/100
        else:
            k_right_mot = 1 + direction/100

        last_error = integral = 0

        self._rMot.run_direct()
        self._lMot.run_direct()

        while (abs(self._rMot.position) + abs(self._lMot.position))/2 <= dist:
            error = self._rMot.position * k_right_mot - self._lMot.position * k_left_mot
            integral = float(0.5) * integral + error
            derivative = error - last_error
            last_error = error
            correction = error * kp + ki * integral + kd * derivative
            if speed < 0:
                correction = -correction

            for (motor, power) in zip((self._lMot, self._rMot), self.steering(direction + correction, speed)):
                motor.duty_cycle_sp = power

        # self._lMot.stop(stop_action="hold")
        # self._rMot.stop(stop_action="hold")

# r._lMot.run_to_rel_pos(speed_sp=800, position_sp=3*360, ramp_up_sp=2000, stop_action="hold")
