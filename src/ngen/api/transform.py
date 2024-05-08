import math
import numpy as np
from OpenGL.GL import *

class Transform:

    X = 0
    Y = 1
    Z = 2

    AXIS_X = [1.0, 0.0, 0.0]
    AXIS_Y = [0.0, 1.0, 0.0]
    AXIS_Z = [0.0, 0.0, 1.0]

    def __init__(self, position: list[float], rotation: list[float], scale: list[float]) -> None:
        self._scale = scale
        self._position = position
        self._rotation = rotation
        self._up = [0, 1, 0]
        self._right = [1, 0, 0]
        self._forward = [0, 0, -1]
        self._update_vectors()

    def get_scale(self) -> list[float]:
        return self._scale

    def set_scale(self, vector: list[float]) -> None:
        self._scale = vector

    def get_position(self) -> list[float]:
        return self._position

    def set_position(self, vector: list[float]) -> None:
        self._position = vector

    def get_rotation(self) -> list[float]:
        return self._rotation

    def set_rotation(self, rotation: list[float]) -> None:
        self._rotation = rotation
        self._update_vectors()

    def get_vector_forward(self) -> list[float]:
        return self._forward

    def get_vector_backwards(self) -> list[float]:
        return [-x for x in self._forward]

    def get_vector_up(self) -> list[float]:
        return self._up

    def get_vector_down(self) -> list[float]:
        return [-x for x in self._up]

    def get_vector_right(self) -> list[float]:
        return self._right

    def get_vector_left(self) -> list[float]:
        return [-x for x in self._right]

    def apply_transformations(self) -> None:
        glTranslatef(*self._position)
        glRotatef(self._rotation[Transform.X], *self.AXIS_X)
        glRotatef(self._rotation[Transform.Y], *self.AXIS_Y)
        glRotatef(self._rotation[Transform.Z], *self.AXIS_Z)
        glScalef(*self._scale)

    def scale(self, factors: list[float]) -> None:
        glScalef(*factors)
        self._scale = [s * f for s, f in zip(self._scale, factors)]

    def translate(self, direction: list[float]) -> None:
        glTranslatef(*direction)
        self._position = [sum(x) for x in zip(self._position, direction)]

    def rotate(self, angle: float, axis: list[float]) -> None:
        glRotatef(angle, *axis)
        self._rotation = [sum(x) for x in zip(self._rotation, [angle * a for a in axis])]
        self._update_vectors()

    def _update_vectors(self) -> None:
        cosY = math.cos(math.radians(self._rotation[Transform.Y]))
        sinY = math.sin(math.radians(self._rotation[Transform.Y]))
        cosP = math.cos(math.radians(self._rotation[Transform.X]))
        sinP = math.sin(math.radians(self._rotation[Transform.X]))
        cosR = math.cos(math.radians(self._rotation[Transform.Z]))
        sinR = math.sin(math.radians(self._rotation[Transform.Z]))

        self._right[Transform.X] = cosR * cosY - sinR * sinP * sinY
        self._right[Transform.Y] = cosP * sinR
        self._right[Transform.Z] = -cosR * sinY - sinR * sinP * cosY

        self._up[Transform.X] = sinR * cosY + cosR * sinP * sinY
        self._up[Transform.Y] = cosP * cosR
        self._up[Transform.Z] = -sinR * sinY + cosR * sinP * cosY

        self._forward[Transform.X] = -cosP * sinY
        self._forward[Transform.Y] = sinP
        self._forward[Transform.Z] = cosP * cosY