from PIL import Image

from .mesh import Mesh
from .texture import Texture

class Loader:

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