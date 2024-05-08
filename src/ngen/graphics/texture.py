from enum import Enum
from OpenGL.GL import *
from PIL import Image, ImageDraw

class Texture:

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
    def generate_missing_albedo(size: int = 256, colors: tuple = ("purple", "black")) -> Image:
        IMAGE = Image.new("RGBA", (size, size), colors[0])
        DRAW = ImageDraw.Draw(IMAGE)
        BLOCK_SIZE = size // 8

        for i in range(0, size, BLOCK_SIZE * 2):
            for j in range(0, size, BLOCK_SIZE * 2):
                DRAW.rectangle([i, j, i + BLOCK_SIZE, j + BLOCK_SIZE], fill = colors[1])
                DRAW.rectangle([i + BLOCK_SIZE, j + BLOCK_SIZE, i + BLOCK_SIZE * 2, j + BLOCK_SIZE * 2], fill = colors[1])

        return IMAGE

class StandardTextures(Enum):
    MISSING_ALBEDO = Texture.generate_missing_albedo()