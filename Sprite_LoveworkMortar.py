#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       Sprite_LoveworkMortar.py
#
#   Author:     Andy Ressa
#   email:      aressa@angrykitten.com
#   Created:    20240101
#
#   Revisions:
#   Date        Init    Notes 
#   20230101    AJR     Initial Draft
#
#==============================================================================

#==============================================================================
# Package Includes
#==============================================================================
from math import floor, pi, ceil, sin, sqrt, atan2
from random import random, randint, uniform, choice

#==============================================================================
# Project Includes
#==============================================================================
from Sprite_FireworkMortar import Sprite_FireworkMortar

#==============================================================================
# Sparkle Effects
#==============================================================================
class Sprite_LoveworkMortar(Sprite_FireworkMortar):
    """

Lovework Particle Map:

 5 . . . . . . * * * . .
 4 . . . . . * . . . * .
 3 . . . . * . . . . . *
 2 . . . . . . . . . . *
 1 . . . . . . . . . . *
 0 . . . . + . . . . *
-1 . . . . . . . . * .
-2 . . . . . . . * .
-3 . . . . . . * .
-4 . . . . . * .
-5 . . . . * .
           0 1 2 3 4 5 6

    """

    _love_stars = [ [0, 3], [1, 4], [2, 5], [3, 5], [4, 5], [5, 4], [6, 3], [6, 2], [6, 1], [5, 0], [4, -1], [3, -2], [2, -3], [1, -4], [0, -5], 
                    [-1, 4], [-2, 5], [-3, 5], [-4, 5], [-5, 4], [-6, 3], [-6, 2], [-6, 1], [-5, 0], [-4, -1], [-3, -2], [-2, -3], [-1, -4] ]


    _lovework_power = 0.035
    _lovework_gravity = 0.2


    #--------------------------------------------------------------------------
    # Init and Constructor
    #--------------------------------------------------------------------------
    def __init__(self, size_m=None, pos_x=None, theta=None, power=None, pow_rng=[0.7, 0.9], star_color=None, trail_color=None):

        super().__init__(size_m=size_m, pos_x=pos_x, theta=theta, power=power, pow_rng=pow_rng, star_color=star_color, trail_color=trail_color)

        self.star_colors = []
        for gb in range(0, 255, 64):
            self.star_colors.append([255, gb, gb, 255])
        self.star_colors.append([255, 255, 255, 255])

        self._pop_shell_func = self.pop_lovework


    def mag(self, vector):
        x, y = vector
        magnitude = sqrt(x**2 + y**2)
        return magnitude

    def angle(self, vector):
        x, y = vector
        angle_radians = atan2(y, x)
        return angle_radians


    #--------------------------------------------------------------------------
    # Pops the Shell to Create Stars
    #--------------------------------------------------------------------------
    def pop_lovework(self, position):
        #print("POP")

        if self.star_color is not None:
            new_color = self.star_color
        else:
            new_color = choice(self.star_colors)

        star_angle = self._launch_physics[0][1] - pi/2

        self.add_particle(position=position, rad_physics=[[0,0,0],[0,0,0]], color=[255, 255, 255, 255], fade=2 )

        new_pos = [position[0], position[1], position[2]]

        new_fade = 0.8

        for star in self._love_stars:

            new_pow = self._lovework_power * self.mag(star)
            new_theta = star_angle + self.angle(star)

            self.stars.append( self.add_star(position=new_pos, power=new_pow, theta=new_theta, color=new_color, fade=new_fade, g=self._lovework_gravity ) )



#==============================================================================
# Stand-Alone Runtime
#==============================================================================

def CreateScene(file=r"c:/temp/govee.gif", cplx_limit=None):

    step_time = .200
    total_time = 9.0

    scene = CurtainScene(panels=1)

    sparkles = Sprite_Sparkles( size_m=scene.phys_size )
    scene.sprites.append( sparkles )

#    scene.sprites.append( Sprite_LoveworkMortar( size_m=scene.phys_size, pos_x=1*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255] ) )
#    scene.sprites.append( Sprite_LoveworkMortar( size_m=scene.phys_size, pos_x=2*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255] ) )
#    scene.sprites.append( Sprite_LoveworkMortar( size_m=scene.phys_size, pos_x=3*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255] ) )
#    scene.run_for_time(8)

    scene.sprites.append( Sprite_LoveworkMortar( size_m=scene.phys_size ) )

    elapsed = 0
    for _ in range( int(total_time/step_time) ):

        if random() > 0.9 and elapsed < (total_time - 7.0):
            scene.sprites.append( Sprite_LoveworkMortar( size_m=scene.phys_size ) )

        if random() > 0.85:
            sparkles.add_sparkle()

        scene.run_for_time(step_time)
        elapsed += step_time

    return scene.export_gif(output_path=file, cplx_limit=cplx_limit)



if __name__ == "__main__":
    from CurtainScene import CurtainScene
    from Sprite_Sparkles import Sprite_Sparkles
    from ComplexityAnalysis import get_gif_complexity
    from os import remove

    print("Sprite_LoveworkMortar Test")

    cplx_lmt = [0, 1250]

    create_cnt = 0
    while create_cnt < 10:
        fn = r"c:/temp/govee_LoveworkMortar_%03d.gif" % create_cnt
        if CreateScene(file=fn, cplx_limit=cplx_lmt ):
            create_cnt += 1

    #CreateScene()