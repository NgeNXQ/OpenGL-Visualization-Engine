import glfw
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from .api import Scene, Entity
from .graphics import Mesh, Texture

class Application:

    _VIEWPORT_OFFSET_X = 0
    _VIEWPORT_OFFSET_Y = 0

    _MIN_DELTA_TIME = 0.005

    _INITIAL_WINDOW_TITLE = ""
    _INITIAL_WINDOW_WIDTH = 1280
    _INITIAL_WINDOW_HEIGHT = 720
    #_INITIAL_ANTI_ALIASING_SAMPLES = 1

    _window_title = _INITIAL_WINDOW_TITLE
    _window_width = _INITIAL_WINDOW_WIDTH
    _window_height = _INITIAL_WINDOW_HEIGHT
    #_anti_aliasing_samples = _INITIAL_ANTI_ALIASING_SAMPLES

    def __init__(self) -> None:
        if not glfw.init():
            return

        glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)
        #glfw.window_hint(glfw.SAMPLES, Settings.get_anti_aliasing_samples())

        self._window = glfw.create_window(self.get_window_width(), self.get_window_height(), self.get_window_title(), None, None)

        if not self._window:
            self._destroy()
            return

        glfw.swap_interval(0)
        glfw.make_context_current(self._window)

        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_COLOR_MATERIAL)

    def get_window_title(self) -> str:
        return self._window_title

    def set_window_title(self, value: str) -> None:
        self._window_title = value

    def get_window_width(self) -> int:
        return self._window_width

    def set_window_width(self, value: int) -> None:
        self._window_width = value

    def get_window_height(self) -> int:
        return self._window_height

    def set_window_height(self, value: int) -> None:
        self._window_height = value

    #def get_anti_aliasing_samples(self) -> int:
    #    return self._anti_aliasing_samples

    #def set_anti_aliasing_samples(self, value: int) -> None:
    #    self._anti_aliasing_samples = value

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

        self.set_window_width(width)
        self.set_window_height(height)

        start_time = glfw.get_time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for scene_object in self._active_scene.get_scene_objects():
            scene_object.update(delta_time if delta_time != 0 else Application._MIN_DELTA_TIME)

        glClearColor(*self._active_scene.get_background_color())

        self._active_scene.get_camera().render()

        for scene_object in self._active_scene.get_scene_objects():
            scene_object.render()

        delta_time = (glfw.get_time() - start_time)

        if delta_time < Application._MIN_DELTA_TIME:
            delta_time = Application._MIN_DELTA_TIME

        glfw.swap_buffers(self._window)

        print(f"FPS: {int(1.0 / delta_time if delta_time != 0 else Application._MIN_DELTA_TIME)}")

    def _destroy(self) -> None:
        for scene_object in self._active_scene.get_scene_objects():
            if isinstance(scene_object, Entity):
                scene_object.get_mesh().free()

        glfw.terminate()

class Loader:

    # Credits: https://github.com/yarolig/OBJFileLoader/tree/master

    @staticmethod
    def load_mesh(relative_path: str) -> Mesh:
        CHAR_FACE = 'f'
        CHAR_VERTEX = 'v'
        CHAR_NORMAL = 'vn'
        CHAR_TEXCOORDS = 'vt'

        faces = []
        normals = []
        vertices = []
        texcoords = []

        with open(relative_path, 'r') as file_stream:
            for line in file_stream:

                if line.startswith('#'):
                    continue

                values = line.split()

                if not values:
                    continue

                if values[0] == CHAR_VERTEX:
                    vertices.append(list(map(float, values[1:4])))
                elif values[0] == CHAR_NORMAL:
                    normals.append(list(map(float, values[1:4])))
                elif values[0] == CHAR_TEXCOORDS:
                    texcoords.append(list(map(float, values[1:3])))
                elif values[0] == CHAR_FACE:

                    face = []
                    norms = []
                    texcoords_face = []

                    for v in values[1:]:
                        w = v.split('/')
                        face.append(int(w[0]))
        
                        if len(w) >= 2 and len(w[1]) > 0:
                            texcoords_face.append(int(w[1]))
                        else:
                            texcoords_face.append(0)

                        if len(w) >= 3 and len(w[2]) > 0:
                            norms.append(int(w[2]))
                        else:
                            norms.append(0)

                    faces.append((face, norms, texcoords_face))

        return Mesh(faces, normals, vertices, texcoords)

    @staticmethod
    def load_texture(relative_path: str) -> Texture:
        return Texture(Image.open(relative_path))