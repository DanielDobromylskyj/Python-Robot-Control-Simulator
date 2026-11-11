from .wheel import Wheel


class Motor:
    def __init__(self, wheel: Wheel, max_torque: float, max_rpm: int, rpm_kp: float = 0.01, reversed: bool=False):
        """
        Kp	    Behaviour   (For RPM Mode)
        0.001	Very slow response
        0.005	Gentle response
        0.01	Moderate response
        0.05	Aggressive response
        0.1	    Very aggressive response

        :param wheel:
        :param max_torque:
        :param max_rpm:
        :param rpm_kp:
        """
        self.wheel: Wheel = wheel

        self.__mode = "torque"

        self.__max_torque = max_torque
        self.__max_rpm = max_rpm

        self.__max_angular_velocity = self.__convert_rpm_to_rad_per_sec(max_rpm)

        self.__target_torque = 0
        self.__target_rpm = 0
        self.__rpm_kp = rpm_kp

        self.__multiplier = -1 if reversed else 1

        self.__has_warned = False
        self.__frame = 0

    @property
    def mode(self):
        return self.__mode

    @property
    def rpm(self):
        return self.wheel.angular_velocity * 9.5493 # 1 rad/sec is 9.5493 rpm

    @staticmethod
    def __convert_rpm_to_rad_per_sec(rpm):
        return rpm / 9.5493

    def set_control_mode_torque(self):
        self.__mode = "torque"

    def set_control_mode_rpm(self):
        self.__mode = "rpm"

    def set_target_torque(self, torque: float):
        if self.mode != "torque" and not self.__has_warned:
            self.__has_warned = True
            print("[WARNING] You are setting a target torque without being in torque control mode!")

        self.__target_torque = torque * self.__multiplier

    def set_target_rpm(self, rpm: float):
        if self.mode != "rpm" and not self.__has_warned:
            self.__has_warned = True
            print("[WARNING] You are setting a target rpm without being in rpm control mode!")

        self.__target_rpm = rpm * self.__multiplier

    @property
    def max_torque(self):
        speed_ratio = min(
            abs(self.wheel.angular_velocity) / self.__max_angular_velocity,
            1.0
        )

        return self.__max_torque * (1.0 - speed_ratio)

    def get_frame(self):
        return self.__frame

    def update(self, dT: float, frame: int):
        """
            Do NOT call from robot. Used for simulation
            Updates the motor, and applies the required torque to its connected wheel
        """
        self.__frame = frame

        if self.mode == "torque":
            torque = self.__target_torque

        elif self.mode == "rpm":
            error = self.__target_rpm - self.rpm
            torque = error * self.__rpm_kp  # Simple P controller, If you want something advanced, make it with torque

        else:
            raise NotImplementedError(f"Invalid Motor Controller Mode! '{self.mode}'")

        max_torque = self.max_torque

        # If regen braking, aka if torque is pushing angular velocity towards 0
        if torque * self.wheel.angular_velocity < 0:
            max_torque = self.__max_torque  # Give all the motors power. Otherwise, it would have no breaks at max RPM

        # Clamp torque to available motor torque
        torque = max(
            min(torque, max_torque),
            -max_torque
        )

        self.wheel.apply_torque(torque)



