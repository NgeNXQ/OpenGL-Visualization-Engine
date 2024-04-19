from ngen.engine import Application, Loader
from ngen.api import Scene, Camera, Transform, Object, Light, SceneObject

def callback_xenomorph_update(scene_object: SceneObject, delta_time: float) -> None:
    scene_object.get_transform().rotate(50 * delta_time, [0.0, 1.0, 0.0])

def main() -> None:
    instance = Application()

    camera = Camera(Transform([0, 0, 0], [0, 0, 0], [1, 1, 1]), 90.0, 0.01, 100.0)

    object = Object(Transform([5, -1, 0], [0, 0, 0], [1.0, 1.0, 1.0]), Loader.load_mesh("assets/xenomorph.obj"),  Loader.load_texture("assets/xenomorph.png"), update_delegate = callback_xenomorph_update)

    light = Light(Transform([0, 0, 0], [0, 0, 0], [1, 1, 1]), 1.0, [1.0, 1.0, 1.0, 1.0], Light.Source.LIGHT_0, Light.Type.SPECULAR)

    scene = Scene([1.0, 1.0, 1.0, 1.0], camera, object, light)

    instance.load_scene(scene)

if __name__ == "__main__":
    main()