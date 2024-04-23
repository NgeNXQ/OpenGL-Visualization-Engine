import math
from abc import ABC
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing import Callable

from .graphics import Mesh, Texture

class Transform:

    X = 0
    Y = 1
    Z = 2

    ROLL = 0
    PITCH = 1
    YAW = 2

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

    def __init__(self, transform: Transform, render_delegate: Callable[["SceneObject"], None] = None, start_delegate: Callable[["SceneObject"], None] = None, *update_delegates: Callable[["SceneObject", float], None]) -> None:
        self._is_active = True
        self._transform = transform
        self._start_delegate = start_delegate
        self._render_delegate = render_delegate
        self._update_delegates = update_delegates

    def get_transform(self) -> Transform:
        return self._transform

    def set_active(self, value: bool) -> None:
        self._is_active = value

    def render(self) -> None:
        if self._is_active:
            self._render_delegate()
            glFlush()

    def start(self) -> None:
        if self._is_active and self._start_delegate is not None:
            self._start_delegate(self)

    def update(self, delta_time: float) -> None:
        if self._is_active:
            for update_delegate in self._update_delegates:
                if update_delegate is not None:
                    update_delegate(self, delta_time)

class Light(SceneObject):

    class Type(Enum):
        AMBIENT = GL_AMBIENT
        DIFFUSE = GL_DIFFUSE
        SPECULAR = GL_SPECULAR

    class Source(Enum):
        LIGHT_0 = GL_LIGHT0
        LIGHT_1 = GL_LIGHT1
        LIGHT_2 = GL_LIGHT2
        LIGHT_3 = GL_LIGHT3
        LIGHT_4 = GL_LIGHT4
        LIGHT_5 = GL_LIGHT5
        LIGHT_6 = GL_LIGHT6
        LIGHT_7 = GL_LIGHT7

    def __init__(self, transform: Transform, intensity: float, color: list[float], light_source: Source, light_type: Type, start_delegate: Callable[["SceneObject"], None] = None, update_delegate: Callable[["SceneObject", float], None] = None) -> None:
        super().__init__(transform, self._render_light, start_delegate, update_delegate)

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

    def _render_light(self) -> None:
        glColor4f(*self._color)
        glLightfv(self._light_source.value, self._light_type.value, [self._intensity] * 3)

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
    
        position = self._transform.get_position()
        forward = self._transform.get_vector_forward()
        look_at_point = [p + f for p, f in zip(position, forward)]
    
        gluLookAt(*position, *look_at_point, *self._transform.get_vector_up())

    #def _render_virtual_camera(self) -> None:
    #    glMatrixMode(GL_PROJECTION)
    #    glLoadIdentity()
    #
    #    aspect_ratio = float(Settings.get_window_width()) / float(Settings.get_window_height())
    #    left = -aspect_ratio * self._clipping_plane_near
    #    right = aspect_ratio * self._clipping_plane_near
    #    bottom = -self._clipping_plane_near
    #    top = self._clipping_plane_near
    #
    #    glFrustum(left, right, bottom, top, self._clipping_plane_near, self._clipping_plane_far)
    #
    #    position = self._transform.get_position()
    #    forward = self._transform.get_vector_forward()
    #    look_at_point = [p + f for p, f in zip(position, forward)]
    #
    #    gluLookAt(*position, *look_at_point, *self._transform.get_vector_up())

class Entity(SceneObject):

    def __init__(self, transform: Transform, mesh: Mesh, texture_albedo: Texture = None, start_delegate: Callable[[SceneObject], None] = None, *update_delegates: Callable[[SceneObject, float], None]) -> None:
        super().__init__(transform, self._render, start_delegate, update_delegates)

        self._mesh = mesh
        self._texture_albedo = texture_albedo

    def get_mesh(self) -> Mesh:
        return self._mesh

    def _render(self) -> None:
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self._texture_albedo is not None:
            glBindTexture(GL_TEXTURE_2D, self._texture_albedo.get_id())
        else:
            glBindTexture(GL_TEXTURE_2D, Texture.Default.MISSING_ALBEDO)

        self._transform.apply_transformations()
        self._mesh.build()

        glBindTexture(GL_TEXTURE_2D, 0)

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

    def destroy(self, scene_object: SceneObject) -> None:
        self._scene_objects.remove(scene_object)

        if (isinstance(scene_object, Entity)):
            scene_object.get_mesh().free()

    def instantiate(self, scene_object: SceneObject) -> None:
        self._scene_objects.append(scene_object)