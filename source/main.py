#from .assets import TestObj

from ngen.engine import Application, Loader

def main() -> None:
    instance = Application()

    #obj = TestObj()

    #mesh = Loader.load_mesh("9/assets/model.obj")
    #texture = Loader.load_texture("9/assets/texture.png")

    #object = Object(Transform([0, 0, -50], [0, 0, 0], [1, 1, 1]), mesh)
    #camera = VirtualCamera(Transform([0, 0, 0], [0, 0, 0], [1, 1, 1]))

    #scene = Scene((0, 0, 0, 1), object)

    #instance.load_scene(scene)

if __name__ == "__main__":
    main()