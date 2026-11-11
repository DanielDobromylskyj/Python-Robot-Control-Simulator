from .connection import Connection

import pygame
import math


class Frame:
    THICKNESS = 0.1 # metre

    def __init__(self,
        connections: list[tuple[tuple[float, float, float], Connection]] | None = None
    ):
        self.__connections: list[tuple[tuple[float, float, float], Connection]] = connections if connections is not None else []

        self.__mass: float
        self.__inertia: float

        self.calculate_mass_and_inertia()

    def get_shape(self):
        min_x = math.inf
        min_y = math.inf
        max_x = -math.inf
        max_y = -math.inf

        for (x, y, a), conn in self.__connections:
            if x > max_x: max_x = x
            if x < min_x: min_x = x
            if y > max_y: max_y = y
            if y < min_y: min_y = y

        return max_x - min_x, max_y - min_y

    def calculate_mass_and_inertia(self) -> float:
        """ Returns mass """
        if len(self.__connections) == 0:
            return 0

        min_x = math.inf
        min_y = math.inf
        max_x = -math.inf
        max_y = -math.inf

        mass = 0.0

        for (x, y, a), conn in self.__connections:
            mass += conn.mass

            if conn.child:
                mass += conn.child.calculate_mass_and_inertia()

            if x > max_x: max_x = x
            if x < min_x: min_x = x
            if y > max_y: max_y = y
            if y < min_y: min_y = y

        # Assume the frame is a box creating this shape made of Aluminum (2712kg/m3)
        body_mass = (max_x - min_x) * (max_y - min_y) * self.THICKNESS * 2712
        mass += body_mass

        self.__mass = mass

        w, d = self.get_shape()
        self.__inertia = (body_mass / 12) * (w**2 + d**2)

        return mass

    @property
    def mass(self):
        return self.__mass

    @property
    def inertia(self):
        return self.__inertia

    @property
    def connections(self):
        return self.__connections

    def add_connection(self, x: float, y: float, angle: float, connection: Connection):
        """ Angle in radians from north / up """
        self.__connections.append(((x, y, angle), connection))
        self.calculate_mass_and_inertia()

    @staticmethod
    def rotate(offset_x, offset_y, rel_x, rel_y, rotation, scale):
        return (
                offset_x + (rel_x * scale) * math.cos(rotation) - (rel_y * scale) * math.sin(rotation),
                offset_y + (rel_y * scale) * math.cos(rotation) + (rel_x * scale) * math.sin(rotation)
        )

    def draw(self, surface: pygame.Surface, offset_x: float, offset_y: float, rotation: float, scale: float=1):
        for (rel_x1, rel_y1, angle1), connection1 in self.__connections:
            x1, y1 = self.rotate(offset_x, offset_y, rel_x1, rel_y1, rotation, scale)

            for (rel_x2, rel_y2, angle2), connection2 in self.__connections:
                x2, y2 = self.rotate(offset_x, offset_y, rel_x2, rel_y2, rotation, scale)
                if connection1 != connection2:
                    pygame.draw.line(
                        surface,
                        (0, 255, 0),
                        (x1, y1),
                        (x2, y2)
                    )

        for (rel_x, rel_y, angle), connection in self.__connections:
            x, y = self.rotate(offset_x, offset_y, rel_x, rel_y, rotation, scale)

            connection.draw( surface, x, y, rotation + angle, scale)
