from .robot import Robot
from .world import World

import math


class Simulator:
    GRAVITY = 9.81

    def __init__(self, world: World, robot: Robot):
        self.world: World = world
        self.robot: Robot = robot

        self.robot_x = 0.0
        self.robot_y = 0.0

        self.robot_vel_x = 0.0
        self.robot_vel_y = 0.0

        self.robot_rotation = 0.0
        self.robot_vel_rotation = 0.0

        self.frame = 0

    def update(self, dT):
        self.frame += 1

        self.robot.update(dT)

        for motor in self.robot.motors:
            if motor.get_frame() != self.frame - 1:
                raise ValueError("Motor has desynced!")

            motor.update(dT, self.frame)

        body = self.robot.body

        mass = body.mass
        inertia = body.inertia

        inv_mass = 1.0 / mass
        inv_inertia = 1.0 / inertia

        wheel_count = len(self.robot.wheels)

        if wheel_count == 0:
            return

        # Assume equal load distribution for now
        normal_force = mass * self.GRAVITY / wheel_count

        for wheel, dx, dy, angle in self.robot.wheels:

            if wheel.inertia <= 0 or wheel.radius <= 0:
                continue

            # Rotate wheel position into world coordinates
            cos_r = math.cos(self.robot_rotation)
            sin_r = math.sin(self.robot_rotation)

            rx = dx * cos_r - dy * sin_r
            ry = dx * sin_r + dy * cos_r

            # Wheel's world-space direction
            wheel_angle = self.robot_rotation + angle

            fx = math.cos(wheel_angle)
            fy = math.sin(wheel_angle)

            # Perpendicular direction (lateral)
            lx = -fy
            ly = fx

            wheel.angular_velocity += (
                wheel.applied_torque / wheel.inertia
            ) * dT

            # Velocity at wheel contact point
            vx = (
                self.robot_vel_x -
                self.robot_vel_rotation * ry
            )

            vy = (
                self.robot_vel_y +
                self.robot_vel_rotation * rx
            )

            # Relative velocity along each wheel axis
            longitudinal_velocity = vx * fx + vy * fy
            lateral_velocity = vx * lx + vy * ly

            # Wheel slip velocity
            slip_long = (
                longitudinal_velocity -
                wheel.angular_velocity * wheel.radius
            )

            slip_lateral = lateral_velocity

            static_mu = math.sqrt(
                wheel.material.static *
                self.world.floor.static
            )

            dynamic_mu = math.sqrt(
                wheel.material.dynamic *
                self.world.floor.dynamic
            )

            def effective_mass_inverse(ax, ay):
                cross = rx * ay - ry * ax

                return (
                    inv_mass +
                    cross * cross * inv_inertia
                )

            k_long = (
                effective_mass_inverse(fx, fy) +
                wheel.radius**2 / wheel.inertia
            )

            k_lateral = effective_mass_inverse(lx, ly)

            # Impulse required to stop slipping
            impulse_long = -slip_long / k_long
            impulse_lateral = -slip_lateral / k_lateral

            # Required combined friction impulse
            impulse_size = math.sqrt(
                impulse_long**2 +
                impulse_lateral**2
            )

            # Maximum static friction impulse (https://en.wikipedia.org/wiki/Friction)
            max_static = static_mu * normal_force * dT

            # Determine whether static friction can hold
            if impulse_size <= max_static:
                wheel.has_traction = True

            else:
                wheel.has_traction = False # Remember to turn it off... Oops

                # Limit friction to dynamic friction
                max_dynamic = dynamic_mu * normal_force * dT

                if impulse_size > 0:
                    scale = max_dynamic / impulse_size

                    impulse_long *= scale
                    impulse_lateral *= scale

            # Convert impulses into world-space force impulses
            jx = (
                impulse_long * fx +
                impulse_lateral * lx
            )

            jy = (
                impulse_long * fy +
                impulse_lateral * ly
            )

            # Apply impulse to chassis velocity
            self.robot_vel_x += jx * inv_mass
            self.robot_vel_y += jy * inv_mass

            # Apply rotational impulse to chassis
            self.robot_vel_rotation += (
                rx * jy - ry * jx
            ) * inv_inertia

            # Apply opposing friction torque to wheel
            wheel.angular_velocity -= (
                impulse_long * wheel.radius /
                wheel.inertia
            )

        # Integrate chassis position and rotation
        self.robot_x -= self.robot_vel_x * dT
        self.robot_y -= self.robot_vel_y * dT

        self.robot_rotation -= self.robot_vel_rotation * dT





