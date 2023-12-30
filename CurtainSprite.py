from CurtainParticle import CurtainParticle

class CurtainSprite:

    particles = []


    def pixelize(self):
        print("Pixelizing Sprite")

        pixels = []
        for particle in self.particles:
            print(particle.pixelize())
            pixels.append( particle.pixelize() )
        
        return pixels



if __name__ == "__main__":
    print("Curtain Sprite Test")

    sprite = CurtainSprite()

    part = CurtainParticle(30, 13)
    sprite.particles.append(part)
    part = CurtainParticle(32, 16)
    sprite.particles.append(part)

    print( sprite.pixelize() )