#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       Sprite_FireworkMortar.py
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
from math import floor, pi, ceil, sin
from random import random, randint, uniform, choice

#==============================================================================
# Project Includes
#==============================================================================
from CurtainSprite import CurtainSprite

#==============================================================================
# Sparkle Effects
#==============================================================================
class Sprite_FireworkMortar(CurtainSprite):

    size_m = None

    shell_particle = None
    stars = []

    gravity = 0.2

    star_colors = [[255, 32, 32, 255], [255, 32, 32, 255], [255, 32, 32, 255], [255, 100, 32, 255], [255, 100, 255, 255]]
  
    trail_color = None
    star_color = None


    #--------------------------------------------------------------------------
    # Init and Constructor
    #--------------------------------------------------------------------------
    def __init__(self, size_m=None, pos_x=None, theta=None, power=None, pow_rng=[0.7, 0.9], star_color=None, trail_color=None):
        super().__init__()

        if size_m is not None and len(size_m) != 2:
            raise Exception(f"size_m must be [x_m, y_m]! (gave me {size_m})")
        self.size_m = size_m if size_m is not None else [1, 1]

        if trail_color is not None:
            self.trail_color = trail_color
        else:
            if random() > 0.75:
                self.trail_color = [255, 200, 0, 255]

        if star_color is not None:
            self.star_color = star_color
        else:
            self.star_color = choice(self.star_colors)

        if power is not None:
            self.power = power
        else:
            if pow_rng is not None:
                self.power = uniform(pow_rng[0], pow_rng[0] )
            else:
                self.power = 0.5

        self.launch_mortar(pos_x=pos_x, theta=theta)


    #--------------------------------------------------------------------------
    # Launches the Mortar
    #--------------------------------------------------------------------------
    def launch_mortar(self, pos_x=None, theta=None):

        if pos_x is not None:
            p_x = pos_x
        else:
            max_x = self.size_m[0]
            off_x = uniform(-0.5, 0.5)
            p_x = (max_x / 2) + off_x

        if theta is not None:
            th = theta
        else:
            tgt_y = 1.5
            th = sin( off_x / tgt_y ) + pi/2


        new_pos = [p_x, 0.0, 0.0]
        new_phys = [[self.power, th, 0], [self.gravity, -pi/2, 0]]
        new_color = [64, 64, 64, 255]
        new_fade = 0.0

        self.shell_particle = self.add_particle(position=new_pos, rad_physics=new_phys, color=new_color, fade=new_fade )


    #--------------------------------------------------------------------------
    # Pops the Shell to Create Stars
    #--------------------------------------------------------------------------
    def pop_shell(self, position, color=None, num_stars=12, num_rings=3, power=0.3 ):
        #print("POP")

        self.add_particle(position=position, rad_physics=[[0,0,0],[0,0,0]], color=[255, 255, 255, 255], fade=2 )

        new_pos = [position[0], position[1], position[2]]

        new_fade = 0.8

        rad_step = 2 * pi / num_stars

        pow_step = power / num_rings

        for ring in range(num_rings):
            for th in range( ceil(num_stars - ring * (num_stars/(num_rings+1))) ):
                self.stars.append( self.add_star(new_pos, (power - (pow_step * ring)), th * rad_step, self.star_color, new_fade ) )
            

    #--------------------------------------------------------------------------
    # Adds a Star
    #--------------------------------------------------------------------------
    def add_star(self, position, power, theta, color, fade, g=None ):
        G = g if g is not None else self.gravity

        new_phys = [[power, theta, 0], [G, -pi/2, 0]]
        return self.add_particle(position=position, rad_physics=new_phys, color=color, fade=fade )


    #--------------------------------------------------------------------------
    # override so we can do more
    #--------------------------------------------------------------------------
    def do_timestep(self, time_s ):
        super().do_timestep(time_s)  # Do the physics first

        if self.shell_particle is not None:

            if self.trail_color is not None:
                self.add_star(self.shell_particle.position, .05, 2 * pi * random(), self.trail_color, 1 )

            v_x, v_y, v_z = self.shell_particle.physics[0]

            if v_y <= 0:
                
                self.pop_shell(position=self.shell_particle.position)

                self.shell_particle = None
                del self.particles[0]

        else:
            #print("whut")
            #input()
            pass

        # Cull Fallen Particles
        for i,part in enumerate(self.particles):
            if part.position[1] < 0:
                del self.particles[i]



#==============================================================================
# Stand-Alone Runtime
#==============================================================================

def CreateScene(file=r"c:/temp/govee.gif", cplx_limit=None):

    step_time = .200
    total_time = 9.0

    scene = CurtainScene(panels=1)

    sparkles = Sprite_Sparkles( size_m=scene.phys_size )
    scene.sprites.append( sparkles )

#    scene.sprites.append( Sprite_FireworkMortar( size_m=scene.phys_size, pos_x=1*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255] ) )
#    scene.sprites.append( Sprite_FireworkMortar( size_m=scene.phys_size, pos_x=2*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255] ) )
#    scene.sprites.append( Sprite_FireworkMortar( size_m=scene.phys_size, pos_x=3*scene.phys_size[0]/4, theta=pi/2, star_color=[255, 100, 255, 255], trail_color=[255, 96, 128, 255] ) )
#    scene.run_for_time(8)

    scene.sprites.append( Sprite_FireworkMortar( size_m=scene.phys_size ) )

    elapsed = 0
    for _ in range( int(total_time/step_time) ):

        if random() > 0.9 and elapsed < (total_time - 7.0):
            scene.sprites.append( Sprite_FireworkMortar( size_m=scene.phys_size ) )

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

    print("Sprite_FireworkMortar Test")

    cplx_lmt = [0, 2500]

    create_cnt = 0
    while create_cnt < 1:
        fn = r"c:/temp/govee_%03d.gif" % create_cnt
        if CreateScene(file=fn, cplx_limit=cplx_lmt ):
            create_cnt += 1

    #CreateScene()