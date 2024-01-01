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
#   20231231    AJR     Fixed Physics (mutable objects, learned sumthin' new)
#                       Allow Particles to be phycially positioned in meters.
#   20240101    AJR     Happy New Year!
#                       Added Spherical Physics Option
#
#==============================================================================

#==============================================================================
# Package Includes
#==============================================================================
from math import floor, sin, cos, pi

#==============================================================================
# Project Includes
#==============================================================================


#==============================================================================
# Curtain Particle Class
# Contains information for an individual particle
#==============================================================================
class CurtainParticle:

    position = None
    color = [128, 128, 255]
    alpha = 255

    physics = []

    fade_rate = None # Percent per Second (normalized)


    #--------------------------------------------------------------------------
    # Init Constructor
    #--------------------------------------------------------------------------
    def __init__(self, position=None, physics=None, rad_physics=None, color=None, fade_rate=None ):

        if position is not None and len(position) < 3:
            raise Exception(f"Positition must be [x, y, z]! (gave me {position})")
        self.position = position if position is not None else [0, 0, 0]

        if physics is not None:
            if rad_physics is not None:
                raise Exception(f"You gave me both physics and rad_physics, plz pick only one.")
            
            for newt in physics:
                if len(newt) != 3:
                    raise Exception(f"All Physics must be [x, y, z]! (gave me {newt})")

            self.physics = physics 
                
        elif rad_physics is not None:

            self.physics = []

            for newt in rad_physics:
                if len(newt) != 3:
                    raise Exception(f"All radPhysics must be [r, theta, rho]! (gave me {newt})")           

                r, theta, rho = newt
                y = r * sin(theta) * cos(rho)
                z = r * sin(theta) * sin(rho)
                x = r * cos(theta)

                self.physics.append( [x, y, z] )

        else:
            self.physics = [ [0.0,0.0,0.0], [0.0,9.8,0.0] ] 

        print(f"New Particle physics: {self.physics}")

        self.fade_rate = fade_rate if fade_rate is not None else 0

        if color is not None and len(color) < 4:
                raise Exception(f"Color must be [r, g, b, a]! (gave me {color})")
        if color is not None:
            self.color = color[0:3]
            self.alpha = color[3]
        else:
            self.color = [255, 255, 255]
            self.alpha = 255

        #print(f"New Particle colored: {self.color} w/ alpha: {self.alpha}")

        #print(f"New particle created @ {self.position}")



    #--------------------------------------------------------------------------
    # Return the Pixel Information for the Particle
    #--------------------------------------------------------------------------
    def pixelize(self):

        color_w_alpha = [floor(element) for element in self.color]
        color_w_alpha.append( self.alpha )

        return [self.position, color_w_alpha]


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


    rad_particle = CurtainParticle(position=[0.0,0.0,0.0], rad_physics=[[1.0, 0.0, 0.0],[0.0,0.0,0.0]])
    rad_particle = CurtainParticle(position=[0.0,0.0,0.0], rad_physics=[[1.0, pi/2, 0.0],[0.0,0.0,0.0]])
    rad_particle = CurtainParticle(position=[0.0,0.0,0.0], rad_physics=[[1.0, pi, 0.0],[0.0,0.0,0.0]])
    rad_particle = CurtainParticle(position=[0.0,0.0,0.0], rad_physics=[[1.0, 3*pi/2, 0.0],[0.0,0.0,0.0]])


    #particle = CurtainParticle([0, 1, 0], physics=[[0, 0, 0], [0, 1]])
