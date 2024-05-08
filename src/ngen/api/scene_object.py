from abc import ABC
from OpenGL.GL import *
from typing import Callable

from .transform import Transform

class SceneObject(ABC):

    def __init__(self, transform: Transform, render_delegate: Callable[[], None] = None, start_delegate: Callable[['SceneObject'], None] = None, *update_delegates: Callable[['SceneObject', float], None]) -> None:
        self._is_active = True
        self._transform = transform
        self._start_delegate = start_delegate
        self._render_delegate = render_delegate
        self._update_delegates = update_delegates

    def get_transform(self) -> Transform:
        return self._transform

    def get_is_active(self, value: bool) -> None:
        self._is_active = value

    def set_is_active(self, value: bool) -> None:
        self._is_active = value

    def render(self) -> None:
        if self._is_active:
            self._render_delegate()
            glFlush()

    def start(self) -> None:
        if self._is_active and self._start_delegate is not None:
            self._start_delegate(self)

    def update(self, delta_time: float) -> None:
        if self._is_active:
            for update_delegate in self._update_delegates:
                update_delegate(self, delta_time)