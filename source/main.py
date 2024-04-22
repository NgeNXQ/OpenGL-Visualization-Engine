from ngen.engine import Application, Loader
from ngen.api import Scene, Camera, Transform, Object, Light, SceneObject
import asyncio


def callback_car1_update(car1: Object, delta_time: float) -> None:
    POSITION_START = 50
    POSITION_FINISH = -25

    VELOCITY = -10
    car1.get_transform().translate([0, 0, VELOCITY * delta_time])

    if car1.get_transform().get_position()[Transform.Z] < POSITION_FINISH:
        car1.get_transform().set_position([0, 0, POSITION_START])


async def main() -> None:
    instance = Application()
    print("Creating camera")
    camera = Camera(Transform([-5, 1.5, 0], [0, 0, 0], [1, 1, 1]), 90.0, 0.01, 100.0)
    print("Camera was created")
    print("Creating car...")
    car1 = Object(Transform([0, 0, 0], [0, 180, 0], [1, 1, 1]),
                  await Loader.load_mesh("../assets/cars/Car 09/Car9.obj"),
                  await Loader.load_texture("../assets/cars/Car 09/Car9.jpeg"),
                  update_delegate=callback_car1_update)
    print("Car was created")

    print("Creating scene...")
    scene = Scene([0.0, 0.0, 0.0, 1.0],
                  camera,
                  car1)
    print("Scene was created")

    print("Initializing scene...")
    await instance.load_scene(scene)


if __name__ == "__main__":
    asyncio.run(main())
