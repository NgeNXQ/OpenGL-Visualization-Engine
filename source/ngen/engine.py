import glfw
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from .api import Settings, Scene
from .graphics import Mesh, Texture

class Application:

    _VIEWPORT_OFFSET_X = 0
    _VIEWPORT_OFFSET_Y = 0

    _MIN_DELTA_TIME = 0.005

    def __init__(self) -> None:
        self._init_glfw()

        #glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_MULTISAMPLE)

        #glShadeModel(GL_SMOOTH)

    def _init_glfw(self) -> None:
        if not glfw.init():
            return

        glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)

        self._window = glfw.create_window(Settings.get_window_width(), Settings.get_window_height(), Settings.get_window_title(), None, None)

        if not self._window:
            self._destroy()
            return

        glfw.make_context_current(self._window)

    def load_scene(self, scene: Scene) -> None:
        self._scene = scene

        for scene_object in self._scene.get_scene_objects():
            scene_object.start()

        while not glfw.window_should_close(self._window):
            self._update()
            glfw.poll_events()

    def _update(self) -> None:
        width, height = glfw.get_framebuffer_size(self._window)
        glViewport(self._VIEWPORT_OFFSET_X, self._VIEWPORT_OFFSET_Y, width, height)

        Settings.set_window_width(width)
        Settings.set_window_height(height)

        start_time = glfw.get_time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self._scene.get_camera().render()

        glClearColor(*self._scene.get_background_color())

        for scene_object in self._scene.get_scene_objects():
            scene_object.render()

        delta_time = (glfw.get_time() - start_time)

        if delta_time < Application._MIN_DELTA_TIME:
            delta_time = Application._MIN_DELTA_TIME

        for scene_object in self._scene.get_scene_objects():
            scene_object.update(delta_time)

        glfw.swap_buffers(self._window)

    def _destroy(self) -> None:
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