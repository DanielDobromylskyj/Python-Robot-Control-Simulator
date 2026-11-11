from robot.motor import Motor
from robot.world import *
from robot.frame import Frame, Connection
from robot.wheel import Wheel
from robot.wheel_material import *
from robot.simulator import Simulator, Robot

import pygame
import math

world = World(
    Rectangle((200, 200), 50, 50),
    Sphere(-100, 50, 40)
)


class DemoRobot(Robot):
    def __init__(self):
        body = Frame()

        fl = Connection(body, child=Wheel(0.3, 0.2, 0.05, rubber))
        fr = Connection(body, child=Wheel(0.3, 0.2, 0.05, rubber))
        bl = Connection(body, child=Wheel(0.3, 0.2, 0.05, rubber))
        br = Connection(body, child=Wheel(0.3, 0.2, 0.05, rubber))

        motors = [
            Motor(fl.child, max_torque=5.0, max_rpm=5000),  # NOQA - Pycharm. I just fucking set Connection().child Its not None
            Motor(fr.child, max_torque=5.0, max_rpm=5000, reversed=True),  # NOQA
            Motor(bl.child, max_torque=5.0, max_rpm=5000),  # NOQA
            Motor(br.child, max_torque=5.0, max_rpm=5000, reversed=True)   # NOQA
        ]

        r_angle = math.pi / 2
        l_angle = -r_angle

        body.add_connection(1, 2, l_angle, fl)
        body.add_connection(-1, 2, r_angle, fr)
        body.add_connection(1, -2, l_angle, bl)
        body.add_connection(-1, -2, r_angle, br)

        super().__init__(body, motors)

    def update(self, dT):
        self.motors[0].set_control_mode_torque()
        self.motors[0].set_target_torque(5)

        self.motors[1].set_control_mode_torque()
        self.motors[1].set_target_torque(5)

sim = Simulator(world, DemoRobot())

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
clock.tick(60)

rot = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    dt = clock.tick(60) / 1000

    # Clear screen
    screen.fill((30, 30, 30))

    # Draw first, as it actually does some (many) rotation calcs for the sim (to save performance)
    sim.robot.body.draw(screen, 500 + sim.robot_x, 500 + sim.robot_y, sim.robot_rotation, 50)
    sim.update(dt)

    pygame.display.flip()

