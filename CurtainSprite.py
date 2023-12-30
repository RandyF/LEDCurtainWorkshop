

class CurtainSprite:

    particles = []
    

    def pixelize(self):
        print("Pixelizing")

        return ((30, 13), (255, 255, 255, 0))



if __name__ == "__main__":
    print("Curtain Sprite Test")

    sprite = CurtainSprite()

    print( sprite.pixelize() )