from enum import Enum
from OpenGL.GL import *
from typing import Callable

from .transform import Transform
from .scene_object import SceneObject

class Light(SceneObject):

    class Type(Enum):
        POINT = 1.0
        DIRECTIONAL = 0.0

    class Source(Enum):
        LIGHT_0 = GL_LIGHT0
        LIGHT_1 = GL_LIGHT1
        LIGHT_2 = GL_LIGHT2
        LIGHT_3 = GL_LIGHT3
        LIGHT_4 = GL_LIGHT4
        LIGHT_5 = GL_LIGHT5
        LIGHT_6 = GL_LIGHT6
        LIGHT_7 = GL_LIGHT7

    def __init__(self, transform: Transform, type: Type, source: Source, color: list[float], start_delegate: Callable[["SceneObject"], None] = None, *update_delegates: Callable[["SceneObject", float], None]) -> None:
        super().__init__(transform, self._render, start_delegate, *update_delegates)

        self._type = type
        self._color = color
        self._source = source

    def get_color(self) -> list[float]:
        return self._color

    def set_color(self, value: list[float]) -> None:
        self._color = value

    def _render(self) -> None:
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glLightfv(self._source.value, GL_POSITION, [*self.get_transform().get_position(), self._type.value])

        glLightfv(self._source.value, GL_AMBIENT, self._color)
        glLightfv(self._source.value, GL_DIFFUSE, self._color)
        glLightfv(self._source.value, GL_SPECULAR, self._color)

        glEnable(self._source.value)