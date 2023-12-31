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
from math import floor
from random import random, randint, uniform

#==============================================================================
# Project Includes
#==============================================================================
from CurtainSprite import CurtainSprite

#==============================================================================
# Sparkle Effects
#==============================================================================
class Sprite_Sparkles(CurtainSprite):

    size_m = None


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
    # Raindrop drip
    #--------------------------------------------------------------------------
    def add_raindrop(self, fade=0.5 ):
        new_pos = [random() * self.size_m[0] , uniform(self.size_m[1], self.size_m[1]*1.25), 0]
        new_phys = [[0, 0, 0], [0, -9.8, 0]]
        new_color = [64, 64, 128, 255]

        self.add_particle(position=new_pos, physics=new_phys, color=new_color, fade=fade )


    #--------------------------------------------------------------------------
    # Init Constructor
    #--------------------------------------------------------------------------
    def add_firefly(self, fade=0.6 ):
        new_pos = [self.size_m[0]*0.25 + random() * 0.75 * self.size_m[0], random() * self.size_m[1], 0]
        new_phys = [[uniform(-1.25,1.25), uniform(-0.25,0.5), 0], [0, -0.25, 0]]
        new_color = [200, 160, 000, 255]

        self.add_particle(position=new_pos, physics=new_phys, color=new_color, fade=fade )


    #--------------------------------------------------------------------------
    # Init Constructor
    #--------------------------------------------------------------------------
    def add_snowflake(self, fade=0.2 ):
        new_pos = [random() * self.size_m[0] , uniform(self.size_m[1], self.size_m[1]*1.25), 0]
        new_phys = [ [uniform(-0.33,0.33), 0, 0], [0, -0.2, 0]]
        new_color = [220, 220, 220, 255]

        self.add_particle(position=new_pos, physics=new_phys, color=new_color, fade=fade )




#==============================================================================
# Stand-Alone Runtime
#==============================================================================
if __name__ == "__main__":
    from CurtainScene import CurtainScene  

    print("Sprite_Sparkles Test")

    step_time = .200
    total_time = 60.0

    scene = CurtainScene(panels=1)

    sprite = Sprite_Sparkles( size_m=scene.phys_size )
    scene.sprites.append( sprite )


    for _ in range( int(total_time/step_time) ):

        scene.run_for_time(step_time)

        if random() > 0.8:
            sprite.add_sparkle()

        if random() > 0.8:
            sprite.add_firefly()

        if random() > 1.0:
            sprite.add_snowflake()

        if random() > 0.2:
            sprite.add_raindrop()


    scene.export_gif(r"c:/temp/govee.gif")
    