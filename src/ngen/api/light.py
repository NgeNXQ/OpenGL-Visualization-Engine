from enum import Enum
from OpenGL.GL import *
from typing import Callable

from .transform import Transform
from .scene_object import SceneObject

class LightSource(Enum):
    LIGHT0 = GL_LIGHT0
    LIGHT1 = GL_LIGHT1
    LIGHT2 = GL_LIGHT2
    LIGHT3 = GL_LIGHT3
    LIGHT4 = GL_LIGHT4
    LIGHT5 = GL_LIGHT5
    LIGHT6 = GL_LIGHT6
    LIGHT7 = GL_LIGHT7

class Light(SceneObject):

    class Type(Enum):
        SPOT = 2.0
        POINT = 1.0
        DIRECTIONAL = 0.0

    def __init__(self, transform: Transform, type: Type, source: LightSource, color: list[float], render_delegate: Callable[[], None] = None, start_delegate: Callable[['Light'], None] = None, *update_delegates: Callable[['Light', float], None]) -> None:
        super().__init__(transform, self._render, start_delegate, *update_delegates)
        self._type = type
        self._color = color
        self._source = source
        self._render_delegate_light = render_delegate

    def get_color(self) -> list[float]:
        return self._color

    def set_color(self, value: list[float]) -> None:
        self._color = value

    def _render(self) -> None:
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glLightfv(self._source.value, GL_POSITION, [*self._transform._position, self._type.value])

        glLightfv(self._source.value, GL_AMBIENT, self._color)
        glLightfv(self._source.value, GL_DIFFUSE, self._color)
        glLightfv(self._source.value, GL_SPECULAR, self._color)

        if self._render_delegate_light is not None:
            self._render_delegate_light()

        glEnable(self._source.value)

class LightDirectional(Light):

    def __init__(self, transform: Transform, source: LightSource, color: list[float], start_delegate: Callable[['LightDirectional'], None] = None, *update_delegates: Callable[['LightDirectional', float], None]) -> None:
        super().__init__(transform, Light.Type.DIRECTIONAL, source, color, None, start_delegate, *update_delegates)

class LightPoint(Light):

    def __init__(self, transform: Transform, source: LightSource, color: list[float], linear_attenuation: float, constant_attenuation: float, quadratic_attenuation: float, start_delegate: Callable[['LightPoint'], None] = None, *update_delegates: Callable[['LightPoint', float], None]) -> None:
        super().__init__(transform, Light.Type.POINT, source, color, self._render_point_light, start_delegate, *update_delegates)
        self._linear_attenuation = linear_attenuation
        self._constant_attenuation = constant_attenuation
        self._quadratic_attenuation = quadratic_attenuation

    def get_constant_attenuation(self) -> float:
        return self._constant_attenuation

    def set_constant_attenuation(self, value: float) -> None:
        self._constant_attenuation = value

    def get_linear_attenuation(self) -> float:
        return self._linear_attenuation

    def set_linear_attenuation(self, value: float) -> None:
        self._linear_attenuation = value

    def get_quadratic_attenuation(self) -> float:
        return self._quadratic_attenuation

    def set_quadratic_attenuation(self, value: float) -> None:
        self._quadratic_attenuation = value

    def _render_point_light(self) -> None:
        glLightf(self._source.value, GL_LINEAR_ATTENUATION, self._linear_attenuation)
        glLightf(self._source.value, GL_CONSTANT_ATTENUATION, self._constant_attenuation)
        glLightf(self._source.value, GL_QUADRATIC_ATTENUATION, self._quadratic_attenuation)

class LightSpot(Light):

    def __init__(self, transform: Transform, source: LightSource, color: list[float], spot_cutoff: float, spot_exponent: float, linear_attenuation: float, constant_attenuation: float, quadratic_attenuation: float,  start_delegate: Callable[['LightSpot'], None] = None, *update_delegates: Callable[['LightSpot', float], None]) -> None:
        super().__init__(transform, Light.Type.SPOT, source, color, self._render_spot_light, start_delegate, *update_delegates)
        self._spot_cutoff = spot_cutoff
        self._spot_exponent = spot_exponent
        self._linear_attenuation = linear_attenuation
        self._constant_attenuation = constant_attenuation
        self._quadratic_attenuation = quadratic_attenuation

    def get_constant_attenuation(self) -> float:
        return self._constant_attenuation

    def set_constant_attenuation(self, value: float) -> None:
        self._constant_attenuation = value

    def get_linear_attenuation(self) -> float:
        return self._linear_attenuation

    def set_linear_attenuation(self, value: float) -> None:
        self._linear_attenuation = value

    def get_quadratic_attenuation(self) -> float:
        return self._quadratic_attenuation

    def set_quadratic_attenuation(self, value: float) -> None:
        self._quadratic_attenuation = value

    def get_spot_cutoff(self) -> float:
        return self._spot_cutoff

    def set_spot_cutoff(self, value: float) -> None:
        self._spot_cutoff = value

    def get_spot_exponent(self) -> float:
        return self._spot_exponent

    def set_spot_exponent(self, value: float) -> None:
        self._spot_exponent = value

    def _render_spot_light(self) -> None:
        glLightf(self._source.value, GL_LINEAR_ATTENUATION, self._linear_attenuation)
        glLightf(self._source.value, GL_CONSTANT_ATTENUATION, self._constant_attenuation)
        glLightf(self._source.value, GL_QUADRATIC_ATTENUATION, self._quadratic_attenuation)
        glLightf(self._source.value, GL_SPOT_CUTOFF, self._spot_cutoff)
        glLightf(self._source.value, GL_SPOT_EXPONENT, self._spot_exponent)
        glLightfv(self._source.value, GL_SPOT_DIRECTION, self._transform.get_vector_forward())