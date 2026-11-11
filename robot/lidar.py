

class Lidar:
    def __init__(self, world, scan_angle_min: float=0.0, scan_angle_max: float=6.283, distance: float = 200):
        self.__world = world

        self.__scan_angle_min = scan_angle_min
        self.__scan_angle_max = scan_angle_max
        self.__distance = distance