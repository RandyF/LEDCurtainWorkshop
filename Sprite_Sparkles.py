#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       Sprite_Sparkles.py
#
#   Author:     Andy Ressa
#   email:      aressa@angrykitten.com
#   Created:    20231231
#
#   Revisions:
#   Date        Init    Notes 
#   20231231    AJR     Initial Draft
#
#==============================================================================

#==============================================================================
# Package Includes
#==============================================================================
from math import floor, pi
from random import random, randint, uniform, choice

#==============================================================================
# Project Includes
#==============================================================================
from CurtainSprite import CurtainSprite

#==============================================================================
# Sparkle Effects
#==============================================================================
class Sprite_Sparkles(CurtainSprite):

    size_m = None

    gravity = -0.5

    snowflakes = []

    #--------------------------------------------------------------------------
    # Init and Constructor
    #--------------------------------------------------------------------------
    def __init__(self, size_m=None):
        super().__init__()

        if size_m is not None and len(size_m) != 2:
            raise Exception(f"size_m must be [x_m, y_m]! (gave me {size_m})")
        self.size_m = size_m if size_m is not None else [1, 1]


    #--------------------------------------------------------------------------
    # Fixed Sparkle that fades
    #--------------------------------------------------------------------------
    def add_sparkle(self, fade=1, color_range=20 ):
        new_pos = [random() * self.size_m[0], random() * self.size_m[1], 0]
        new_phys = [[0, 0, 0], [0, 0, 0]]
        new_color = [randint(255-color_range, 255), randint(255-color_range, 255), randint(255-color_range, 255), 255]

        self.add_particle(position=new_pos, physics=new_phys, color=new_color, fade=fade )


    #--------------------------------------------------------------------------
    # Add Raindrop drip
    #--------------------------------------------------------------------------
    def add_raindrop(self, fade=0.333 ):
        new_pos = [random() * self.size_m[0] , uniform(self.size_m[1], self.size_m[1]*1.2), 0]
        new_phys = [[0, 0, 0], [0, self.gravity, 0]]
        new_color = [64, 64, 128, 255]

        self.add_particle(position=new_pos, physics=new_phys, color=new_color, fade=fade )


    #--------------------------------------------------------------------------
    # Add Firefly Particle
    #--------------------------------------------------------------------------
    def add_firefly(self, fade=0.6 ):
        new_pos = [self.size_m[0]*0.25 + random() * 0.75 * self.size_m[0], random() * self.size_m[1], 0]
        new_phys = [[0.333, choice([0, pi]) + uniform(-0.0*pi/8, 2*pi/8), 0], [-0.25*self.gravity, -pi/2, 0]]
        new_color = [200, 160, 000, 255]

        self.add_particle(position=new_pos, rad_physics=new_phys, color=new_color, fade=fade )


    #--------------------------------------------------------------------------
    # Add Snowflake Particle
    #--------------------------------------------------------------------------
    def add_snowflake(self, fade=0.2 ):
        new_pos = [random() * self.size_m[0] , uniform(self.size_m[1], self.size_m[1]*1.25), 0]
        new_phys = [ [uniform(-0.33,0.33), 0, 0], [0, 0.25*self.gravity, 0]]
        new_color = [220, 220, 220, 255]

        self.snowflakes.append( self.add_particle(position=new_pos, physics=new_phys, color=new_color, fade=fade ) )


    #--------------------------------------------------------------------------
    # override so we can do more
    #--------------------------------------------------------------------------
    def do_timestep(self, time_s ):
        super().do_timestep(time_s)  # Do the physics first

        for snowflake in self.snowflakes:
            if random() < 0.25:
                snowflake.physics[0][0] = -snowflake.physics[0][0]


#==============================================================================
# Stand-Alone Runtime
#==============================================================================
if __name__ == "__main__":
    from CurtainScene import CurtainScene  
    print("Sprite_Sparkles Test")

    def CreateSparkleScene(file=r"c:/temp/govee_sparkles.gif", cplx_limit=None):

        step_time = .200
        total_time = 13

        scene = CurtainScene(panels=1)

        sprite = Sprite_Sparkles( size_m=scene.phys_size )
        scene.sprites.append( sprite )


        sparkle_chance = 0.0
        firefly_chance = 0.0
        snowflk_chance = 0.2
        raindrp_chance = 0.0


        elapsed = 0.0
        while elapsed < total_time:

            #print(elapsed)
            if elapsed >= 5 and elapsed < 5.1:
                #print(len(scene.raw_frames) )
                scene.raw_frames = []
                #print(len(scene.raw_frames) )

            if random() < sparkle_chance:
                sprite.add_sparkle()

            if random() < firefly_chance:
                sprite.add_firefly()

            if random() < snowflk_chance:
                sprite.add_snowflake()

            if random() < raindrp_chance:
                sprite.add_raindrop()

            scene.run_for_time(step_time)
            elapsed += step_time

        return scene.export_gif(output_path=file, cplx_limit=cplx_limit)


    cplx_lmt = [0, 600]

    create_cnt = 0
    while create_cnt < 10:
        fn = r"c:/temp/govee_snow_%03d.gif" % create_cnt
        if CreateSparkleScene(file=fn, cplx_limit=cplx_lmt ):
            create_cnt += 1
    