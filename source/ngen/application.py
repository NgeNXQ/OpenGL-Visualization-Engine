import glfw
from OpenGL.GL import *

from .scene import Scene
from .entity import Entity
from .preferences import Preferences

class Application:

    _instance = None

    _VIEWPORT_OFFSET_X = 0
    _VIEWPORT_OFFSET_Y = 0

    _MIN_DELTA_TIME = 0.005
    _delta_time = _MIN_DELTA_TIME

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Application, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not glfw.init():
            return

        glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.SAMPLES, Preferences.get_anti_aliasing_samples())

        self._window = glfw.create_window(Preferences.get_window_width(), Preferences.get_window_height(), Preferences.get_window_title(), None, None)

        if not self._window:
            self._destroy()
            return

        glfw.make_context_current(self._window)
        glfw.swap_interval(0)

        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_COLOR_MATERIAL)

    def get_fps(self) -> int:
        return int(1 / self._delta_time)

    def get_delta_time(self) -> float:
        return self._delta_time

    def load_scene(self, scene: Scene) -> None:
        self._active_scene = scene

        for scene_object in self._active_scene.get_scene_objects():
            scene_object.start()

        while not glfw.window_should_close(self._window):
            self._update()
            glfw.poll_events()

    def _update(self) -> None:
        width, height = glfw.get_framebuffer_size(self._window)
        glViewport(self._VIEWPORT_OFFSET_X, self._VIEWPORT_OFFSET_Y, width, height)

        Preferences.set_window_width(width)
        Preferences.set_window_height(height)
        glfw.set_window_title(self._window, f"{Preferences.get_window_title()} {self.get_fps()}")

        start_time = glfw.get_time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for scene_object in self._active_scene.get_scene_objects():
            scene_object.update(self._delta_time)

        glClearColor(*self._active_scene.get_background_color())

        self._active_scene.get_camera().render()

        for scene_object in self._active_scene.get_scene_objects():
            scene_object.render()

        finish_time = glfw.get_time()

        self._delta_time = (finish_time - start_time)

        if  self._delta_time < Application._MIN_DELTA_TIME:
             self._delta_time = Application._MIN_DELTA_TIME

        glfw.swap_buffers(self._window)

    def _destroy(self) -> None:
        for scene_object in self._active_scene.get_scene_objects():
            if isinstance(scene_object, Entity):
                scene_object.get_mesh().free()

        glfw.terminate()