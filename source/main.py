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

    camera = Camera(Transform([0.0, 5.0, -20.0], [-15.0, 0.0, 0.0], [1, 1, 1]), 45.0, 0.01, 100.0)

    road_1 = Object(Transform([0, 0, 0], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_2 = Object(Transform([0, 0, -6.36], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_3 = Object(Transform([0, 0, -12.72], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_4 = Object(Transform([0, 0, 6.36], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_5 = Object(Transform([0, 0, 12.72], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_6 = Object(Transform([0, 0, 19.08], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_7 = Object(Transform([0, 0, 25.44], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))
    road_8 = Object(Transform([0, 0, 31.8], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/road/road.obj"), Loader.load_texture("assets/road/road.jpeg"))

    grass_patch_1 = Object(Transform([5, 0.25, -12], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))
    grass_patch_2 = Object(Transform([5, 0.25, -8], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))
    grass_patch_3 = Object(Transform([5, 0.25, -4], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))
    grass_patch_4 = Object(Transform([5, 0.25, 0], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))
    grass_patch_5 = Object(Transform([5, 0.25, 4], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))
    grass_patch_6 = Object(Transform([5, 0.25, 8], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))
    grass_patch_7 = Object(Transform([5, 0.25, 12], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))

    grass_patch_8 = Object(Transform([5, 0.25, 12], [180, 0, 0], [2, 1, 2]), Loader.load_mesh("assets/grass/grass_patch.obj"), Loader.load_texture("assets/grass/grass_patch_summer.png"))

    car1 = Object(Transform([0, 0, 0], [0, 180, 0], [1, 1, 1]), Loader.load_mesh("assets/cars/Car 01/car.obj"), Loader.load_texture("assets/cars/Car 01/car_blue.png"), update_delegate = callback_car1_update)

    scene = Scene([1.0, 1.0, 1.0, 1.0], camera, 
                                        road_1, 
                                        road_2, 
                                        road_3, 
                                        road_4, 
                                        road_5, 
                                        road_6, 
                                        road_7, 
                                        road_8, 
                                        grass_patch_1,
                                        grass_patch_2,
                                        grass_patch_3,
                                        grass_patch_4,
                                        grass_patch_5,
                                        grass_patch_6,
                                        grass_patch_7,
                                        car1)

    instance.load_scene(scene)

if __name__ == "__main__":
    main()