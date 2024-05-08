from OpenGL.GL import *
from typing import Callable

from ..graphics.mesh import Mesh
from .transform import Transform
from .scene_object import SceneObject
from ..graphics.texture import Texture, StandardTextures

class Entity(SceneObject):

    def __init__(self, transform: Transform, mesh: Mesh, texture_albedo: Texture = None, start_delegate: Callable[['Entity'], None] = None, *update_delegates: Callable[['Entity', float], None]) -> None:
        super().__init__(transform, self._render, start_delegate, *update_delegates)
        self._mesh = mesh
        self._texture_albedo = texture_albedo if texture_albedo is not None else Texture(StandardTextures.MISSING_ALBEDO.value)

    def get_mesh(self) -> Mesh:
        return self._mesh

    def _render(self) -> None:
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPolygonMode(GL_FRONT, GL_FILL)

        glBindTexture(GL_TEXTURE_2D, self._texture_albedo.get_id())

        self._transform.apply_transformations()
        self._mesh.build()

        glBindTexture(GL_TEXTURE_2D, 0)