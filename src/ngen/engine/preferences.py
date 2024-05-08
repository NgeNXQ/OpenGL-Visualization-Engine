class Preferences:

    _window_title = ""
    _window_width = 1280
    _window_height = 720
    _anti_aliasing_samples = 1

    @classmethod
    def get_window_title(cls) -> str:
        return cls._window_title

    @classmethod
    def set_window_title(cls, value: str) -> None:
        cls._window_title = value

    @classmethod
    def get_window_width(cls) -> int:
        return cls._window_width

    @classmethod
    def set_window_width(cls, value: int) -> None:
        cls._window_width = value

    @classmethod
    def get_window_height(cls) -> int:
        return cls._window_height

    @classmethod
    def set_window_height(cls, value: int) -> None:
        cls._window_height = value

    @classmethod
    def get_aspect_ratio(cls) -> float:
        return cls._window_width / cls._window_height

    @classmethod
    def get_anti_aliasing_samples(self) -> int:
        return self._anti_aliasing_samples

    def set_anti_aliasing_samples(self, value: int) -> None:
        self._anti_aliasing_samples = value