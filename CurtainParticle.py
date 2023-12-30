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
from math import floor

#==============================================================================
# Project Includes
#==============================================================================


#==============================================================================
# Curtain Particle Class
# Contains information for an individual particle
#==============================================================================
class CurtainParticle:

    position = [0, 0, 0]
    color = [128, 128, 255]
    alpha = 255

    physics = [ [0,-5.0,0], [0,0,0] ]

    fade_rate = 0.333  # Percent per Second (normalized)


    #--------------------------------------------------------------------------
    # Pixelize all Particles in the Sprite
    #--------------------------------------------------------------------------
    def __init__(self, pos_x = 0, pos_y = 0, pos_z = 0):
        self.position = [pos_x, pos_y, pos_z]


    #--------------------------------------------------------------------------
    # Return the Pixel Information for the Particle
    #--------------------------------------------------------------------------
    def pixelize(self):

        color_w_alpha = [floor(element) for element in self.color]
        color_w_alpha.append( self.alpha )

        pos_quant = [floor(element) for element in self.position]

        return [pos_quant, color_w_alpha]


    #--------------------------------------------------------------------------
    # Applies fade to the COLOR of the particle
    # TODO: consider using alpha, but that's not implemented at a higher level
    #--------------------------------------------------------------------------
    def apply_fade(self, time_s ):
        
        fade_mult = 1-(self.fade_rate * time_s);
        #print(fade_mult)
    
        self.color = [element * fade_mult for element in self.color]
        #print(self.color)

    #--------------------------------------------------------------------------
    # Performs the Pixel Time Step
    #--------------------------------------------------------------------------
    def apply_physics(self, time_s):

        self.position[0] = self.position[0] + self.physics[0][0] * time_s
        self.position[1] = self.position[1] + self.physics[0][1] * time_s
        self.position[2] = self.position[2] + self.physics[0][2] * time_s

        for i, phys in enumerate(self.physics[1:]):
            #print(i, phys)

            self.physics[i][0] = self.physics[i][0] + self.physics[i+1][0] * time_s
            self.physics[i][1] = self.physics[i][1] + self.physics[i+1][1] * time_s
            self.physics[i][2] = self.physics[i][2] + self.physics[i+1][2] * time_s


    #--------------------------------------------------------------------------
    # Performs the Pixel Time Step
    #--------------------------------------------------------------------------
    def do_timestep(self, time_s ):
        self.apply_fade(time_s)
        self.apply_physics(time_s)



#==============================================================================
# Stand-Alone Runtime
#==============================================================================
if __name__ == "__main__":
    print("Curtain Particle Test")

    particle = CurtainParticle()
  
    print( particle.position, particle.pixelize() )

    particle.do_timestep(0.200)

    print( particle.position, particle.pixelize() )
    particle.do_timestep(0.200)

    print( particle.position, particle.pixelize() )
    particle.do_timestep(0.200)

    print( particle.position, particle.pixelize() )
    particle.do_timestep(0.200)

    print( particle.position, particle.pixelize() )
