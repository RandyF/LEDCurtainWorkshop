#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       CurtainSprite.py
#
#   Author:     Andy Ressa
#   email:      aressa@angrykitten.com
#   Created:    20231230
#
#   Revisions:
#   Date        Init    Notes 
#   20231230    AJR     Initial Draft
#   20231231    AJR     Created add_particle Method
#
#==============================================================================

#==============================================================================
# Package Includes
#==============================================================================


#==============================================================================
# Project Includes
#==============================================================================
from CurtainParticle import CurtainParticle


#==============================================================================
# Curtain Sprite Class
# A group of Particles that are handled together
#==============================================================================
class CurtainSprite:

    particles = None

    #--------------------------------------------------------------------------
    # Init Constructor
    #--------------------------------------------------------------------------
    def __init__(self):
        self.particles = []


    #--------------------------------------------------------------------------
    # Pixelize all Particles in the Sprite
    #--------------------------------------------------------------------------
    def pixelize(self):
        #print("Pixelizing Sprite")

        pixels = []
        for particle in self.particles:
            #print(particle.pixelize())
            pixels.append( particle.pixelize() )
        
        return pixels


    #--------------------------------------------------------------------------
    # Performs the Pixel Time Step
    #--------------------------------------------------------------------------
    def do_timestep(self, time_s ):

        for particle in self.particles:
            particle.do_timestep(time_s)

    def add_particle(self, position=None, physics=None, fade=None ):

        new_part = CurtainParticle(position, physics, fade )
        self.particles.append( new_part )


#==============================================================================
# Stand-Alone Runtime
#==============================================================================

if __name__ == "__main__":
    print("Curtain Sprite Test")

    sprite = CurtainSprite()

    sprite.add_particle([30, 13, 0])
    sprite.add_particle([32, 16, 0])

    print( sprite.pixelize() )