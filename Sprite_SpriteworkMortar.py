#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       Sprite_SpriteworkMortar.py
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
class Sprite_SpriteworkMortar(Sprite_FireworkMortar):

    _spritework_star_map = None
    _spritework_gravity = 0.2


    #--------------------------------------------------------------------------
    # Init and Constructor
    #--------------------------------------------------------------------------
    def __init__(self, size_m=None, pos_x=None, theta=None, power=None, pow_rng=[0.7, 0.9], star_color=None, trail_color=None, spritemap=None, sprite_pow=None, sprite_grav=None):

        super().__init__(size_m=size_m, pos_x=pos_x, theta=theta, power=power, pow_rng=pow_rng, star_color=star_color, trail_color=trail_color)

        if spritemap is not None:
            self._spritework_star_map = spritemap
        else:
            x = [200, 180, 100, 255]
            z = [200, 150, 100, 255]
            y = 0 #[0, 120, 180, 255]
            s = 0 #[164, 128, 0, 255]
            k = [255, 255, 255, 255]

            self._spritework_star_map = [ [ 0, 16, k], [ 0, 14, k], [ -1, 12, x], [ 0, 12, k], [ 1, 12, x], [ -2, 11, x], [ 0, 11, x], [ 2, 11, x],													
                            [ -3, 10, x], [ 3, 10, x],	[ -3, 9, x], [ 3, 9, x],[ -2, 8, x], [ -1, 8, z], [ 0, 8, z], [ 1, 8, z],
                            [ 2, 8, x], [ -2, 7, x], [ 2, 7, x], [ -2, 6, x], [ 0, 6, y], [ 2, 6, x], [ -2, 5, x], [ 1, 5, y], [ 2, 5, x],													
                            [ -2, 4, x], [ 2, 4, x], [ -2, 3, x], [ -1, 3, y],	[ 2, 3, x],	 [ -2, 2, x], [ 0, 2, y], [ 2, 2, x],													
                            [ -2, 1, x], [ 0, 1, y], [ 2, 1, x],[ -2, 0, x], [ 0, 0, y], [ 2, 0, x], [ -2, -1, x], [ -1, -1, y],
                            [ 2, -1, x], [ -3, -2, x], [ 3, -2, x], [ -4, -3, x], [ 1, -3, s], [ 4, -3, x], [ -4, -4, x], [ -3, -4, s], 
                            [ 2, -4, s], [ 4, -4, x], [ -4, -5, x], [ -2, -5, s], [ 1, -5, s], [ 4, -5, x], [ -4, -6, x], [ 0, -6, x],
                            [ 4, -6, x], [ -3, -7, x], [ -2, -7, x], [ -1, -7, x], [ 1, -7, x], [ 2, -7, x], [ 3, -7, x] ]


        if sprite_pow is not None:
            self._shell_power = sprite_pow
        else:
            self._shell_power = 0.035

        if sprite_grav is not None:
            self._spritework_gravity = sprite_grav
        else:
            self._spritework_gravity = 0.035

        self.star_colors = []
        for gb in range(0, 255, 64):
            self.star_colors.append([255, gb, gb, 255])
#        self.star_colors.append([255, 255, 255, 255])

        if star_color is not None:
            self.star_color = star_color
        else:
            self.star_color = choice(self.star_colors)

        for i, star in enumerate(self._spritework_star_map):
            if star[2] is None:
                self._spritework_star_map[i][2] = self.star_color


        self._pop_shell_func = self.pop_sprite


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
    def pop_sprite(self, position):
        #print("POP")

        star_angle = self._launch_physics[0][1] - pi/2

        self.add_particle(position=position, rad_physics=[[0,0,0],[0,0,0]], color=[255, 255, 255, 255], fade=2 )

        new_pos = [position[0], position[1], position[2]]

        new_fade = 0.6

        for x, y, color in self._spritework_star_map:

            new_pow = self._shell_power * self.mag([x, y])
            new_theta = star_angle + self.angle([x, y])

            if color != 0:
                self.stars.append( self.add_star(position=new_pos, power=new_pow, theta=new_theta, color=color, fade=new_fade, g=self._spritework_gravity ) )



#==============================================================================
# Stand-Alone Runtime
#==============================================================================


def CreateScene(file=r"c:/temp/govee.gif", cplx_limit=None, star_map=None):

    step_time = .200
    total_time = 9.0

    scene = CurtainScene(panels=1)

    sparkles = Sprite_Sparkles( size_m=scene.phys_size )
    scene.sprites.append( sparkles )

#    scene.sprites.append( Sprite_SpriteworkMortar( size_m=scene.phys_size, pos_x=1*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255], spritemap=star_map ) )
#    scene.sprites.append( Sprite_SpriteworkMortar( size_m=scene.phys_size, pos_x=2*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 255, 255, 255], spritemap=star_map ) )
#    scene.sprites.append( Sprite_SpriteworkMortar( size_m=scene.phys_size, pos_x=3*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255], spritemap=star_map ) )
#    scene.run_for_time(8)

    scene.sprites.append( Sprite_SpriteworkMortar( size_m=scene.phys_size, spritemap=star_map, pow_rng=[0.6, 0.8] ) )

    elapsed = 0
    for _ in range( int(total_time/step_time) ):

        # if random() > 0.9 and elapsed < (total_time - 7.0):
        #     scene.sprites.append( Sprite_SpriteworkMortar( size_m=scene.phys_size, spritemap=star_map ) )

        # if random() > 0.85:
        #     sparkles.add_sparkle()

        scene.run_for_time(step_time)
        elapsed += step_time

    return scene.export_gif(output_path=file, cplx_limit=cplx_limit)



lovework_map = [ [0, 3, None], [1, 4, None], [2, 5, None], [3, 5, None], [4, 5, None], [5, 4, None],
            [6, 3, None], [6, 2, None], [6, 1, None], [5, 0, None], [4, -1, None], [3, -2, None],
            [2, -3, None], [1, -4, None], [0, -5, None], [-1, 4, None], [-2, 5, None], [-3, 5, None],
            [-4, 5, None], [-5, 4, None], [-6, 3, None], [-6, 2, None], [-6, 1, None], [-5, 0, None],
            [-4, -1, None], [-3, -2, None], [-2, -3, None], [-1, -4, None] ]



if __name__ == "__main__":
    from CurtainScene import CurtainScene
    from Sprite_Sparkles import Sprite_Sparkles
    from ComplexityAnalysis import get_gif_complexity
    from os import remove

    print("Sprite_SpriteworkMortar Test")

    cplx_lmt = [0, 2000]

    create_cnt = 0
    while create_cnt < 10:
        fn = r"c:/temp/govee_SpriteworkMortar_%03d.gif" % create_cnt
        if CreateScene(file=fn, cplx_limit=cplx_lmt ):
            create_cnt += 1

    #CreateScene()