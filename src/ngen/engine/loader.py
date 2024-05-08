from PIL import Image

from ..graphics.mesh import Mesh
from ..graphics.texture import Texture

class Loader:

    @staticmethod
    def load_mesh(relative_path: str) -> Mesh:
        CHAR_FACE = 'f'
        CHAR_VERTEX = 'v'
        CHAR_NORMAL = 'vn'
        CHAR_COMMENT = '#'
        CHAR_SEPARATOR = '/'
        CHAR_TEXCOORDS = 'vt'

        INDEX_VERTEX = 0
        INDEX_TEXCOORD = 1
        INDEX_NORMAL = 2

        faces = []
        normals = []
        vertices = []
        texcoords = []

        with open(relative_path, 'r') as file_stream:
            for line in file_stream:

                if not line.startswith(CHAR_COMMENT):
                    values = line.split()

                    if values:
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

                            for value in values[1:]:
                                face_components = value.split(CHAR_SEPARATOR)

                                face.append(int(face_components[INDEX_VERTEX]))
                                norms.append((int(face_components[INDEX_NORMAL]) if len(face_components) >= 3 and face_components[INDEX_NORMAL] else 0))
                                texcoords_face.append((int(face_components[INDEX_TEXCOORD]) if len(face_components) >= 2 and face_components[INDEX_TEXCOORD] else 0))

                            faces.append((face, norms, texcoords_face))

        return Mesh(faces, normals, vertices, texcoords)

    @staticmethod
    def load_texture(relative_path: str) -> Texture:
        return Texture(Image.open(relative_path))