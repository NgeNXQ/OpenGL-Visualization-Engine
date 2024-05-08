from OpenGL.GL import *
from OpenGL.GLU import *
from typing import Callable

from .transform import Transform
from .scene_object import SceneObject
from ..engine.preferences import Preferences

class Camera(SceneObject):

    def __init__(self, transform: Transform, clipping_plane_near: float, clipping_plane_far: float, render_delegate: Callable[[], None], start_delegate: Callable[['Camera'], None] = None, *update_delegates: Callable[['Camera', float], None]) -> None:
        super().__init__(transform, self._render, start_delegate, *update_delegates)
        self._clipping_plane_far = clipping_plane_far
        self._clipping_plane_near = clipping_plane_near
        self._camera_render_delegate = render_delegate

    def _render(self) -> None:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self._camera_render_delegate()
        gluLookAt(*self._transform.get_position(), *[(position + forward) for position, forward in zip(self._transform._position, self._transform.get_vector_forward())], *self._transform.get_vector_up())

class CameraPerspective(Camera):

    def __init__(self, transform: Transform, fov: float, clipping_plane_near: float, clipping_plane_far: float, start_delegate: Callable[['CameraPerspective'], None] = None, *update_delegates: Callable[['CameraPerspective', float], None]) -> None:
        super().__init__(transform, clipping_plane_near, clipping_plane_far, self._render_perspective_camera, start_delegate, *update_delegates)
        self._fov = fov

    def get_fov(self) -> float:
        return self._fov

    def set_fov(self, value: float) -> None:
        self._fov = value

    def _render_perspective_camera(self) -> None:
        gluPerspective(self._fov, Preferences.get_aspect_ratio(), self._clipping_plane_near, self._clipping_plane_far)

class CameraOrthographic(Camera):

    def __init__(self, transform: Transform, clipping_plane_near: float, clipping_plane_far: float, start_delegate: Callable[['CameraOrthographic'], None] = None, *update_delegates: Callable[['CameraOrthographic', float], None]) -> None:
        super().__init__(transform, clipping_plane_near, clipping_plane_far, self._render_orthographic_camera, start_delegate, *update_delegates)

    def _render_orthographic_camera(self) -> None:
        VIEWPORT_CENTER_WIDTH = Preferences.get_window_width() / 2.0
        VIEWPORT_CENTER_HEIGHT = Preferences.get_window_height() / 2.0
        glOrtho(-VIEWPORT_CENTER_WIDTH, VIEWPORT_CENTER_WIDTH, -VIEWPORT_CENTER_HEIGHT, VIEWPORT_CENTER_HEIGHT, self._clipping_plane_near, self._clipping_plane_far)