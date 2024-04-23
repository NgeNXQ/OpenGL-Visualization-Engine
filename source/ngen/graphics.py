import numpy as np
from enum import Enum
from OpenGL.GL import *
from PIL import Image, ImageDraw

class Mesh:

    # Credits: https://github.com/yarolig/OBJFileLoader/tree/master

    def __init__(self, faces: list[tuple], normals: list[float], vertices: list[float], texcoords: list[float]) -> None:
        self._faces = faces
        self._normals = np.array(normals, dtype = np.float32)
        self._vertices = np.array(vertices, dtype = np.float32)
        self._texcoords = np.array(texcoords, dtype = np.float32)

        glEnable(GL_TEXTURE_2D)

        self._display_list = glGenLists(1)
        glNewList(self._display_list, GL_COMPILE)

        glFrontFace(GL_CCW)

        for face in self._faces:
            vertices, normals, texture_coords = face

            glBegin(GL_POLYGON)

            for i in range(len(vertices)):

                if normals[i] > 0:
                    glNormal3fv(self._normals[normals[i] - 1])

                if texture_coords[i] > 0:
                    glTexCoord2fv(self._texcoords[texture_coords[i] - 1])

                glVertex3fv(self._vertices[vertices[i] - 1])

            glEnd()
        glEndList()
    
        glDisable(GL_TEXTURE_2D)

    # Deprecated

    #def build(self) -> None:
    #    glEnable(GL_TEXTURE_2D)
    #
    #    for face in self._faces:
    #        vertices, normals, texture_coords = face
    #
    #        glBegin(GL_POLYGON)
    #
    #        for i in range(len(vertices)):
    #
    #            if normals[i] > 0:
    #                glNormal3fv(self._normals[normals[i] - 1])
    #
    #            if texture_coords[i] > 0:
    #                glTexCoord2fv(self._texcoords[texture_coords[i] - 1])
    #
    #            glVertex3fv(self._vertices[vertices[i] - 1])
    #
    #        glEnd()
    #
    #    glDisable(GL_TEXTURE_2D)

    def build(self) -> None:
        glCallList(self._display_list)

    def free(self) -> None:
        if self._display_list is not None:
            glDeleteLists([self._display_list])

class Texture:

    class Default(Enum):
        MISSING_ALBEDO = Texture(Texture._generate_default_albedo())

    def __init__(self, texture: Image) -> None:
        self._texture = texture
        self._texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture.width, texture.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture.tobytes("raw", "RGBA", 0, -1))
        glGenerateMipmap(GL_TEXTURE_2D)

    def get_id(self) -> int:
        return self._texture_id

    @staticmethod
    def _generate_default_albedo(size: int = 64, colors: tuple = ("purple", "black")) -> Image:
        IMAGE = Image.new("RGBA", (size, size), colors[0])
        DRAW = ImageDraw.Draw(IMAGE)
        BLOCK_SIZE = size // 8

        for i in range(0, size, BLOCK_SIZE * 2):
            for j in range(0, size, BLOCK_SIZE * 2):
                DRAW.rectangle([i, j, i + BLOCK_SIZE, j + BLOCK_SIZE], fill = colors[1])
                DRAW.rectangle([i + BLOCK_SIZE, j + BLOCK_SIZE, i + BLOCK_SIZE * 2, j + BLOCK_SIZE * 2], fill = colors[1])

        return IMAGE