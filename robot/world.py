from .wheel_material import asphalt

import math

class Object:
    def collides_with(self, xy1: tuple[float, float], xy2: tuple[float, float]) -> None | tuple[float, float]:
        raise NotImplementedError()

class Sphere(Object):
    def __init__(self, cx: float, cy: float, r: float):
        self.cx = cx
        self.cy = cy
        self.r  = r

    def collides_with(self, xy1: tuple[float, float], xy2: tuple[float, float]) -> None | tuple[float, float]:
        x1, y1 = xy1
        x2, y2 = xy2

        dx = x2 - x1
        dy = y2 - y1

        length_sq = dx * dx + dy * dy

        if length_sq == 0:
            distance = ((x1 - self.cx) ** 2 + (y1 - self.cy) ** 2) ** 0.5
            return distance if distance <= self.r else None

        # Project circle centre onto the line segment
        t = ((self.cx - x1) * dx + (self.cy - y1) * dy) / length_sq
        t = max(0, min(1, t))

        # Closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        distance = ((closest_x - self.cx) ** 2 + (closest_y - self.cy) ** 2) ** 0.5

        return distance if distance <= self.r else None

class Rectangle(Object):
    def __init__(self, top_left: tuple[float, float], width: float, height: float, rotation: float=0):
        self.x, self.y = top_left
        self.width, self.height = width, height
        self.rotation = rotation  # radians, relative to top left point

    def collides_with(self, xy1: tuple[float, float], xy2: tuple[float, float]) -> None | tuple[float, float]:
        # Translate endpoints relative to rectangle origin
        x1, y1 = xy1[0] - self.x, xy1[1] - self.y
        x2, y2 = xy2[0] - self.x, xy2[1] - self.y

        # Rotate into rectangle's local coordinate space
        cos_r = math.cos(-self.rotation)
        sin_r = math.sin(-self.rotation)

        x1, y1 = x1 * cos_r - y1 * sin_r, x1 * sin_r + y1 * cos_r
        x2, y2 = x2 * cos_r - y2 * sin_r, x2 * sin_r + y2 * cos_r

        dx = x2 - x1
        dy = y2 - y1

        t_min, t_max = 0.0, 1.0

        # Slab intersection test
        for p, d, low, high in (
            (x1, dx, 0, self.width),
            (y1, dy, 0, self.height)
        ):
            if d == 0:
                if p < low or p > high:
                    return None
                continue

            t1 = (low - p) / d
            t2 = (high - p) / d

            t_min = max(t_min, min(t1, t2))
            t_max = min(t_max, max(t1, t2))

            if t_min > t_max:
                return None

        # Closest intersection point, transformed back to world space
        ix = xy1[0] + (xy2[0] - xy1[0]) * t_min
        iy = xy1[1] + (xy2[1] - xy1[1]) * t_min

        return ix, iy

class World:
    def __init__(self, *args):
        self.__objects: list[Object] = [
            obj for obj in args
        ]

        self.floor = asphalt

    def add_object(self, obj):
        self.__objects.append(obj)

    def ray(self, xy1: tuple[float, float], direction: float, distance: float) -> None | float:
        """ Direction is in rads from north """
        # Find max distance that the ray can see (end point)
        xy2 = (
            xy1[0] + math.sin(direction) * distance,
            xy1[1] + math.cos(direction) * distance
        )

        # Find the closest object
        min_dist = math.inf
        for obj in self.__objects:
            if hit := obj.collides_with(xy1, xy2):
                dist = math.sqrt( (hit[0] - xy1[0]) ** 2 + (hit[1] - xy1[1]) ** 2 )

                if min_dist > dist: min_dist = dist

        # If still math.inf, it's not hit anything, return None
        if min_dist == math.inf:
            return None

        return min_dist
