from .frame import Frame
from .motor import Motor, Wheel

class Robot:
    def __init__(self, body: Frame, motors: list[Motor]):
        self.body: Frame = body

        self.wheels: list[tuple[Wheel, float, float, float]] = []
        self.motors = motors

        self.reload_body()

    def __search_for_wheels(self, frame: Frame, ox, oy, angle):
        """ Recursively scans the frame for wheels"""
        if isinstance(frame, Wheel):
            self.wheels.append((frame, ox, oy, angle))

        else:
            for (dx, dy, da), connection in frame.connections:
                if connection.child:
                    ox, oy = Frame.rotate(ox, oy, dx, dy, angle, 1)

                    self.__search_for_wheels(connection.child, ox, oy, angle+da)

    def reload_body(self):
        """ Reloads the Robot if you have made changes to the Frame. Must be called manually """
        self.wheels = []
        self.__search_for_wheels(self.body, 0, 0, 0)

    def update(self, dT):
        """ This is the function that will control the robot"""
        pass



