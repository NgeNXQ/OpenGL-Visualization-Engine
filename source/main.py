from ngen.engine import Application, Loader
from ngen.api import Scene, Camera, Transform, Object, Light, SceneObject


def callback_car1_update(car1: Object, delta_time: float) -> None:
    POSITION_START = 50
    POSITION_FINISH = -25

    VELOCITY = -10
    car1.get_transform().translate([0, 0, VELOCITY * delta_time])

    if car1.get_transform().get_position()[Transform.Z] < POSITION_FINISH:
        car1.get_transform().set_position([0, 0, POSITION_START])


def main() -> None:
    instance = Application()

    camera = Camera(Transform([-5, 1.5, 0], [0, 0, 0], [1, 1, 1]), 90.0, 0.01, 100.0)

    car1 = Object(Transform([0, 0, 0], [0, 180, 0], [1, 1, 1]), Loader.load_mesh("../assets/cars/Car 09/Car9.obj"),
                  Loader.load_texture("../assets/cars/Car 09/Car9.jpeg"), update_delegate=callback_car1_update)

    scene = Scene([0.0, 0.0, 0.0, 1.0], camera,
                  car1)

    instance.load_scene(scene)


if __name__ == "__main__":
    main()
