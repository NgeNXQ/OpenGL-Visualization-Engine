from OpenGL.GL import *

class Mesh:

    def __init__(self, faces: list[tuple], normals: list[float], vertices: list[float], texcoords: list[float]) -> None:
        self._faces = faces
        self._normals = normals
        self._vertices = vertices
        self._texcoords = texcoords

        self._display_list = glGenLists(1)
        glNewList(self._display_list, GL_COMPILE)

        glFrontFace(GL_CCW)
        glEnable(GL_TEXTURE_2D)

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

        glDisable(GL_TEXTURE_2D)

        glEndList()

    def build(self) -> None:
        glCallList(self._display_list)

    def free(self) -> None:
        if self._display_list is not None:
            glDeleteLists([self._display_list])