from .frame import Frame
from .wheel_material import Material

import math
import pygame

DEG_90_IN_RAD = math.pi / 2

class Wheel(Frame):
    MAX_ANGULAR_VELOCITY = 100

    def __init__(self, radius: float, depth: float, wall_thickness: float, material: Material):
        super().__init__()

        self.radius = radius
        self.inner_radius = radius-wall_thickness
        self.depth = depth
        self.material = material

        if wall_thickness > radius:
            raise ValueError("Invalid material thickness for given wheel radius!")

        self.volume = math.pi * depth * (radius**2 - (radius-wall_thickness)**2)
        self.__mass = self.volume * self.material.density
        self.__inertia = 0.5 * self.mass * (radius ** 2 + self.inner_radius ** 2)

        self.angular_velocity = 0.0
        self.applied_torque = 0.0

        self.last_rotation = 0.0
        self.has_traction = True

    @property
    def mass(self):
        return self.__mass

    @property
    def inertia(self):
        return self.__inertia


    def apply_torque(self, torque):
        self.applied_torque += torque

    def draw(self, surface: pygame.Surface, offset_x: float, offset_y: float, rotation: float, scale: float = 1):
        rotation += DEG_90_IN_RAD
        self.last_rotation = rotation

        scaled = max(-1, min(1, self.angular_velocity / self.MAX_ANGULAR_VELOCITY))
        colour = (round(255 * abs(scaled)), 100, 100)

        if not self.has_traction:
            colour = (255, 0, 0)

        tl = self.rotate(offset_x, offset_y, self.depth, self.radius, rotation, scale)
        bl = self.rotate(offset_x, offset_y, 0, self.radius, rotation, scale)
        tr = self.rotate(offset_x, offset_y, self.depth, -self.radius, rotation, scale)
        br = self.rotate(offset_x, offset_y, 0, -self.radius, rotation, scale)

        centre = self.rotate(offset_x, offset_y, self.depth/2, 0, rotation, scale)
        direction = self.rotate(offset_x, offset_y, self.depth / 2, self.radius*scaled, rotation, scale)


        pygame.draw.lines(
            surface,
            colour,
            True,
            [tl, bl, br, tr],
        )

        pygame.draw.line(
            surface,
            colour,
            centre,
            direction
        )