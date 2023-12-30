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

    particles = []

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



#==============================================================================
# Stand-Alone Runtime
#==============================================================================

if __name__ == "__main__":
    print("Curtain Sprite Test")

    sprite = CurtainSprite()

    part = CurtainParticle(30, 13)
    sprite.particles.append(part)
    part = CurtainParticle(32, 16)
    sprite.particles.append(part)

    print( sprite.pixelize() )