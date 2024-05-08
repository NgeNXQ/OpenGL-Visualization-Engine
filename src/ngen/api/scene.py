from .camera import Camera
from .entity import Entity
from .scene_object import SceneObject

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