#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       CurtainParticle.py
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


#==============================================================================
# Curtain Particle Class
# Contains information for an individual particle
#==============================================================================
class CurtainParticle:

    position = [0, 0, 0]
    color = [255, 255, 255, 255]

    fade_rate = 0.0  # Percent per Second


    #--------------------------------------------------------------------------
    # Pixelize all Particles in the Sprite
    #--------------------------------------------------------------------------
    def __init__(self, pos_x = 0, pos_y = 0, pos_z = 0):
        self.position = [pos_x, pos_y, pos_z]


    #--------------------------------------------------------------------------
    # Return the Pixel Information for the Particle
    #--------------------------------------------------------------------------
    def pixelize(self):

        return [self.position, self.color]




#==============================================================================
# Stand-Alone Runtime
#==============================================================================
if __name__ == "__main__":
    print("Curtain Particle Test")

    particle = CurtainParticle()

    print( particle.pixelize() )