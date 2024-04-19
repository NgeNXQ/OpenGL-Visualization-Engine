from ngen.engine import Application, Loader
from ngen.api import Scene, Camera, Transform, Object, Light, SceneObject

def callback_xenomorph_black_update(xenomorph_black: Object, delta_time: float) -> None:
    xenomorph_black.get_transform().rotate(50 * delta_time, [0.0, 1.0, 0.0])

def callback_xenomorph_white_update(xenomorph_white: Object, delta_time: float) -> None:
    xenomorph_white.get_transform().rotate(-50 * delta_time, [0.0, 1.0, 0.0])

def main() -> None:
    instance = Application()

    camera = Camera(Transform([-5, 1.5, 0], [0, 0, 0], [1, 1, 1]), 90.0, 0.01, 100.0)

    xenomorph_white = Object(Transform([0, 0, 2], [0, 0, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("assets/xenomorph.obj"), update_delegate = callback_xenomorph_white_update)
    xenomorph_black = Object(Transform([0, 0, 0], [0, 0, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("assets/xenomorph.obj"), Loader.load_texture("assets/xenomorph.png"), update_delegate = callback_xenomorph_black_update)

    scene = Scene([1.0, 0.0, 0.0, 1.0], camera, xenomorph_white, xenomorph_black)

    instance.load_scene(scene)

if __name__ == "__main__":
    main()