

class CurtainParticle:

    position = [0, 0, 0]
    color = [255, 255, 255, 255]

    fade_rate_per_sec = 0

    def __init__(self, pos_x = 0, pos_y = 0, pos_z = 0):
        self.position = [pos_x, pos_y, pos_z]

    def pixelize(self):

        return [self.position, self.color]




if __name__ == "__main__":
    print("Curtain Particle Test")

    particle = CurtainParticle()

    print( particle.pixelize() )