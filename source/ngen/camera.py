from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Callable

from .transform import Transform
from .scene_object import SceneObject

class Camera(SceneObject):

    class Type(Enum):
        FRUSTUM = 0
        ORTHOGONAL = 1
        PERSPECTIVE = 2

    def __init__(self, transform: Transform, type: Type, fov: float, clipping_plane_near: float, clipping_plane_far: float, start_delegate: Callable[["SceneObject"], None] = None, *update_delegates: Callable[["SceneObject", float], None]) -> None:
        super().__init__(transform, self._render, start_delegate, self._update_aspect_ratio, *update_delegates)

        self._fov = fov
        self._type = type
        self._clipping_plane_far = clipping_plane_far
        self._clipping_plane_near = clipping_plane_near

        self._aspect_ratio = float(1280) / 720

    def get_fov(self) -> float:
        return self._fov

    def set_fov(self, value: float) -> None:
        self._fov = value

    def _update_aspect_ratio(self, delta_time: float) -> None:
        pass

    def _render(self) -> None:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self._type == Camera.Type.FRUSTUM:
            glFrustum(-self._aspect_ratio, self._aspect_ratio, -1, 1, self._clipping_plane_near, self._clipping_plane_far)
        elif self._type == Camera.Type.ORTHOGONAL:
            glOrtho(-self._aspect_ratio, self._aspect_ratio, -1, 1, self._clipping_plane_near, self._clipping_plane_far)
        elif self._type == Camera.Type.PERSPECTIVE:
            gluPerspective(self._fov, self._aspect_ratio, self._clipping_plane_near, self._clipping_plane_far)