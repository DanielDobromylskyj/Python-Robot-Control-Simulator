from typing import TYPE_CHECKING

import pygame
import math

if TYPE_CHECKING:
    from .frame import Frame


ARROW_ANGLE_IN_RAD = math.pi / 4
OFFSET = math.pi / 4


class Connection:
    def __init__(self, parent: "Frame", child: "Frame | None" = None, angle: float = 0, angle_min: float = -1.5707, angle_max: float = 1.5707, mass: float = 5.0):
        self.parent: "Frame" = parent
        self.child: "Frame | None" = child

        self.mass = mass
        self.angle = 0
        self.angle_min = angle_min
        self.angle_max = angle_max

        # Ensure the angle is actually within bounds
        self.set_angle(angle)

    def set_angle(self, angle: float):
        self.angle = min(max(angle, self.angle_min), self.angle_max)

    @staticmethod
    def __get_end(x: float, y: float, angle: float, length: float) -> tuple[float, float]:
        return (
            x + length * math.cos(angle) - length * math.sin(angle),
            y + length * math.cos(angle) + length * math.sin(angle)
        )

    def __draw_arrow(self, surface: pygame.Surface, colour: tuple[int, int, int], x: float, y: float, angle: float, scale: float = 1):
        end   = self.__get_end(x, y, angle,                     scale*0.5 )
        left  = self.__get_end(*end, angle+ARROW_ANGLE_IN_RAD, -scale*0.1 )
        right = self.__get_end(*end, angle-ARROW_ANGLE_IN_RAD, -scale*0.1 )

        pygame.draw.line(
            surface,
            colour,
            (x, y),
            end
        )
        pygame.draw.line(
            surface,
            colour,
            end,
            left
        )
        pygame.draw.line(
            surface,
            colour,
            end,
            right
        )

    def draw(self, surface: pygame.Surface, offset_x: float, offset_y: float, rotation: float, scale: float):
        if self.child:
            self.child.draw(surface, offset_x, offset_y, rotation + self.angle, scale)

        rotation += OFFSET

        self.__draw_arrow(surface, (100, 100, 0  ), offset_x, offset_y, rotation + self.angle,     scale)
        self.__draw_arrow(surface, (100, 100, 100), offset_x, offset_y, rotation + self.angle_min, scale)
        self.__draw_arrow(surface, (100, 100, 100), offset_x, offset_y, rotation + self.angle_max, scale)
