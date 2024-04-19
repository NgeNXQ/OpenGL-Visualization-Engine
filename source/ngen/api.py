import math
from abc import ABC
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing import Callable

from .graphics import Mesh, Texture

class Transform:

    X = 0
    Y = 1
    Z = 2

    def __init__(self, position: list[float], rotation: list[float], scale: list[float]) -> None:
        self._scale = scale
        self._position = position
        self._rotation = rotation

        self._up = [0, 1, 0]
        self._right = [1, 0, 0]
        self._forward = [0, 0, -1]

        self._update_vectors()

    def _update_vectors(self) -> None:
        cosY = math.cos(math.radians(self._rotation[Transform.Y]))
        sinY = math.sin(math.radians(self._rotation[Transform.Y]))
        cosP = math.cos(math.radians(self._rotation[Transform.X]))
        sinP = math.sin(math.radians(self._rotation[Transform.X]))

        self._forward[Transform.X] = cosY * cosP
        self._forward[Transform.Y] = sinP
        self._forward[Transform.Z] = -sinY * cosP

        cosR = math.cos(math.radians(self._rotation[Transform.Z]))
        sinR = math.sin(math.radians(self._rotation[Transform.Z]))

        self._up[Transform.X] = -cosY * sinR - sinY * sinP * cosR
        self._up[Transform.Y] = cosP * cosR
        self._up[Transform.Z] = -sinY * sinR + cosY * sinP * cosR

        self._right[Transform.X] = cosY * cosR + sinY * sinP * sinR
        self._right[Transform.Y] = sinR * cosP
        self._right[Transform.Z] = -sinY * cosR + cosY * sinP * sinR

    def get_scale(self) -> list[float]:
        return self._scale
    
    def set_scale(self, vector: list[float]) -> None:
        self.scale(vector)
    
    def get_position(self) -> list[float]:
        return self._position
    
    def set_position(self, vector: list[float]) -> None:
        self.translate(vector)
    
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
        glRotatef(self._rotation[Transform.X], 1, 0, 0)
        glRotatef(self._rotation[Transform.Y], 0, 1, 0)
        glRotatef(self._rotation[Transform.Z], 0, 0, 1)
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

class SceneObject(ABC):

    def __init__(self, transform: Transform, render_delegate: Callable[["SceneObject"], None] = None, start_delegate: Callable[["SceneObject"], None] = None, update_delegate: Callable[["SceneObject", float], None] = None) -> None:
        self._transform = transform
        self._start_delegate = start_delegate
        self._render_delegate = render_delegate
        self._update_delegate = update_delegate

    def get_transform(self) -> Transform:
        return self._transform

    def set_transform(self, value: Transform) -> None:
        self._transform = value

    def render(self) -> None:
        self._render_delegate()

    def start(self) -> None:
        if self._start_delegate is not None:
            self._start_delegate(self)

    def update(self, delta_time: float) -> None:
        if self._update_delegate is not None:
            self._update_delegate(self, delta_time)

class Camera(SceneObject):

    def __init__(self, transform: Transform, fov: float, clipping_plane_near: float, clipping_plane_far: float, start_delegate: Callable[["SceneObject"], None] = None, update_delegate: Callable[["SceneObject", float], None] = None) -> None:
        super().__init__(transform, self._render_virtual_camera, start_delegate, update_delegate)

        self._fov = fov
        self._clipping_plane_far = clipping_plane_far
        self._clipping_plane_near = clipping_plane_near

    def _render_virtual_camera(self) -> None:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(self._fov, float(Settings.get_window_width()) / float(Settings.get_window_height()), self._clipping_plane_near, self._clipping_plane_far)

        position = self.transform.get_position()

        up = self.transform.get_vector_up()
        forward = self.transform.get_vector_forward()

        look_at_point = [p + f for p, f in zip(position, forward)]

        gluLookAt(*position, *look_at_point, *up)

        glMatrixMode(GL_MODELVIEW)

class Object(SceneObject):

    def __init__(self, transform: Transform, mesh: Mesh, texture_albedo: Texture = None, start_delegate: Callable[["SceneObject"], None] = None, update_delegate: Callable[["SceneObject", float], None] = None) -> None:
        super().__init__(transform, self._render_object, start_delegate, update_delegate)

        self._mesh = mesh
        self._texture_albedo = texture_albedo

    def _render_object(self) -> None:

        if self._texture_albedo is not None:
            glBindTexture(GL_TEXTURE_2D, self._texture_albedo.get_texture_id())

        self._mesh.build()

        glBindTexture(GL_TEXTURE_2D, 0)

class LightSource(SceneObject):

    def __init__(self, transform: Transform, intensity: float, color: list[float], light_source: int, light_type: int, start_delegate: Callable[["SceneObject"], None] = None, update_delegate: Callable[["SceneObject", float], None] = None) -> None:
        super().__init__(transform, self._render_light_source_point, start_delegate, update_delegate)

        self._color = color
        self._intensity = intensity
        self._light_type = light_type
        self._light_source = light_source

    def get_intensity(self) -> float:
        return self._intensity

    def set_intensity(self, value: float) -> None:
        self._intensity = value

    def get_color(self) -> list[float]:
        return self._color

    def set_color(self, value: list[float]) -> None:
        self._color = value

    def _render_light_source_point(self) -> None:
        glColor3f(*self._color)
        glLightfv(self._light_source, self._light_type, [self._intensity] * 3)

class Scene:

    def __init__(self, background_color: list[float], camera: Camera, *scene_objects: SceneObject) -> None:
        self._camera = camera
        self._background_color = background_color
        self._scene_objects = list(scene_objects)

    def get_camera(self) -> Camera:
        return self._camera

    def get_scene_objects(self) -> list:
        return self._scene_objects

    def get_background_color(self) -> list[float]:
        return self._background_color

    def set_background_color(self, value: list[float]) -> None:
        self._background_color = value

    def destroy(self, sceneObject: SceneObject) -> None:
        self._scene_objects.remove(sceneObject)

    def instantiate(self, sceneObject: SceneObject) -> None:
        self._scene_objects.append(sceneObject)

class Settings(ABC):

    _INITIAL_WINDOW_TITLE = ""
    _INITIAL_WINDOW_WIDTH = 1280
    _INITIAL_WINDOW_HEIGHT = 720
    _INITIAL_ANTI_ALIASING_LEVEL = 1

    _window_title = _INITIAL_WINDOW_TITLE
    _window_width = _INITIAL_WINDOW_WIDTH
    _window_height = _INITIAL_WINDOW_HEIGHT
    _anti_aliasing_level = _INITIAL_ANTI_ALIASING_LEVEL

    @classmethod
    def get_window_title(cls) -> str:
        return cls._window_title

    @classmethod
    def set_window_title(cls, value: str) -> None:
        cls._window_title = value

    @classmethod
    def get_window_width(cls) -> int:
        return cls._window_width

    @classmethod
    def set_window_width(cls, value: int) -> None:
        cls._window_width = value

    @classmethod
    def get_window_height(cls) -> int:
        return cls._window_height

    @classmethod
    def set_window_height(cls, value: int) -> None:
        cls._window_height = value

    @classmethod
    def get_anti_aliasing_level(cls) -> int:
        return cls._anti_aliasing_level

    @classmethod
    def set_anti_aliasing_level(cls, value: int) -> None:
        cls._anti_aliasing_level = value