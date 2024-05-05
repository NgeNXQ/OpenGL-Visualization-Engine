from ngen import Application, Camera, Entity, Transform, Light, Scene, Loader

def main() -> None:
    application = Application()

    camera = Camera(Transform([0, 0, -1000], [0, 0, 0], [1, 1, 1]), Camera.Type.FRUSTUM, 90, 0.01, 100.0)
    uav = Entity(Transform([0, 0, 0], [0, 0, 0], [0.01, 0.01, 0.01]), Loader.load_mesh("assets/rocket.obj"), Loader.load_texture("assets/rocket.png"))
    light_source = Light(Transform([0, 0, 0], [0, 0, 0], [1, 1, 1]), Light.Type.DIRECTIONAL, Light.Source.LIGHT_0, [1, 1, 1])
    scene = Scene([1, 1, 1, 1], camera, uav, light_source)

    application.load_scene(scene)

if __name__ == "__main__":
    main()