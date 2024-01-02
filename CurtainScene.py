#==============================================================================
#
#   Project:    LEDCurtainWorkshop
#   File:       CurtainScene.py
#
#   Author:     Andy Ressa
#   email:      aressa@angrykitten.com
#   Created:    20231230
#
#   Revisions:
#   Date        Init    Notes 
#   20231230    AJR     Initial Draft
#   20231231    AJR     Object Init Cleanup
#                       Allow Particles to be phycially positioned in meters.
#   20240102    AJR     Added some attempts to understand complexity
#
#==============================================================================

#==============================================================================
# Package Includes
#==============================================================================
from PIL import Image
from math import ceil
from random import random, randint
from copy import copy
from os import remove, rename
#import numpy as np


#==============================================================================
# Project Includes
#==============================================================================
from CurtainSprite import CurtainSprite
from CurtainParticle import CurtainParticle

from ComplexityAnalysis import get_gif_complexity

#==============================================================================
# Curtain Scene Class
# Manages Sprites and Renders Images
#==============================================================================
class CurtainScene:

    px_width, px_height = None, None
    phys_width, phys_height = None, None
    time_step_s = None

    sprites = None

    raw_frames = None


    #--------------------------------------------------------------------------
    # Init Constructor
    #--------------------------------------------------------------------------
    def __init__(self, panels=3, time_step_s=None ):
        self.sprites = []
        self.raw_frames = []

        self.px_width, self.px_height = panels*20, 26
        self.phys_width, self.phys_height = panels*1.47, 1.85

        self.time_step_s = time_step_s if time_step_s is not None else 0.200


    @property
    def phys_size(self):
        # Getter method
        return [self.phys_width, self.phys_height]


    #--------------------------------------------------------------------------
    # Render Frames for a certain duration
    #--------------------------------------------------------------------------
    def run_for_time(self, time_secs):

        steps = ceil(time_secs / self.time_step_s)
        #print("running ", steps, "steps")

        for _ in range(steps):

            for sprite in self.sprites:
                sprite.do_timestep(self.time_step_s)

            self.render_frame()
        

    #--------------------------------------------------------------------------
    # Scale the Sprites (which are in meters) to pixels
    #--------------------------------------------------------------------------
    def get_scaled_pixels(self):
        scale_x = self.px_width / self.phys_width
        scale_y = self.px_height / self.phys_height
        
        #print(f"scale_x, scale_y: {scale_x}, {scale_y}")

        scaled_pixels = []

        for sprite in self.sprites:
            for pixel in sprite.pixelize():
                #print(f"unscaled: {pixel}")

                scaled_pos = [int(pixel[0][0] * scale_x), int(pixel[0][1] * scale_y), int(pixel[0][2]) ]
                #print([ scaled_pos, pixel[1] ])

                scaled_pixels.append( [ scaled_pos, pixel[1] ] )

        #print(scaled_pixels)

        return scaled_pixels


    #--------------------------------------------------------------------------
    # Render the Current Frame
    #--------------------------------------------------------------------------
    def render_frame(self):
        #print("render_frame")

        frame_pixels = [ [[0, 0, 0, 255]] * self.px_width for _ in range(self.px_height)]

        for (pos_x, pos_y, pos_z), (c_r, c_g, c_b, c_a) in self.get_scaled_pixels():

            #print( (pos_x, pos_y, pos_z), (c_r, c_g, c_b, c_a) )

            cur_y = self.px_height-1-pos_y
            cur_x = pos_x
            #print(cur_x, cur_y)

            if cur_y not in range(self.px_height) or cur_x not in range(self.px_width):
                continue

            #print(cur_x, cur_y)

            cur_r, cur_g, cur_b, cur_a = frame_pixels[cur_y][cur_x]
            #print(cur_r, cur_g, cur_b, cur_a)

            cur_r = c_r  # TODO: alpha
            cur_g = c_g  # TODO: alpha
            cur_b = c_b  # TODO: alpha

            #print(cur_r, cur_g, cur_b)

            frame_pixels[cur_y][cur_x] = [cur_r, cur_g, cur_b, 255]

        self.raw_frames.append(frame_pixels)



    #--------------------------------------------------------------------------
    # Calculate "complexity" as the number of changes between frames.
    # I think this is the ulitmate limitation for Govee Imports
    #--------------------------------------------------------------------------
    def calc_frame_complexity(self, frame_a, frame_b):

        cplx = 0

        for y, row in enumerate(frame_a):
            for x, element in enumerate(row):

                if element != frame_b[y][x]:
                    cplx += 1
        
        return cplx


    def stack_complexity(self):

        complxity = self.px_width * self.px_height

        for i, frame in enumerate(self.raw_frames):
            if i > 0:
                complxity += self.calc_frame_complexity( self.raw_frames[i-1], self.raw_frames[i] )

        return complxity


    #--------------------------------------------------------------------------
    # Export the current frame image array as a gif
    #--------------------------------------------------------------------------
    def export_gif(self, output_path, duration=200, loop=0, cplx_limit=None ):


        if cplx_limit is not None:
            if isinstance(cplx_limit, list):
                c_min = cplx_limit[0]
                c_max = cplx_limit[1]
            else:
                c_min = 0
                c_max = cplx_limit


        # if cplx_limit is not None:
        #     stk_cplx = self.stack_complexity()
        #     if stk_cplx > c_max or stk_cplx < c_min:
        #         #print("Complexity over Limit!")
        #         return False

        #print(output_path, " exporting ", len(self.raw_frames), "frames in ", duration, " cplx: ", self.stack_complexity() )

        img_frames = []
        for i, frame in enumerate(self.raw_frames):

            #fully unroll the frame
            flat_pixels = [element for row in frame for element in row]
            framedat = [element for row in flat_pixels for element in row]
                    
            frame_image = Image.frombytes("RGBA", (self.px_width, self.px_height), bytes(framedat) )

            img_frames.append(frame_image)


        # Save the animated GIF
        img_frames[0].save(
            output_path,
            save_all=True,
            format='gif', 
            optimize=False,
            append_images=img_frames[1:],
            duration=duration,
            loop=loop,
        )
        
        gif_complexity = get_gif_complexity(output_path)
        if cplx_limit is not None:

            if gif_complexity > c_max or gif_complexity < c_min:
                remove(output_path)
                return False
            else:
                rename( output_path, "%s_%d.gif" % (output_path[:-4], gif_complexity))

        print(output_path, " exported ", len(self.raw_frames), "frames in ", duration, " cplx: ", self.stack_complexity(), "/", gif_complexity)

        return True
    


#==============================================================================
# Stand-Alone Runtime
#==============================================================================
if __name__ == "__main__":
    print("Curtain Scene Test")

    scene = CurtainScene(panels=1)

    sprite = CurtainSprite()
    scene.sprites.append( sprite )

    step_time = .200
    total_time = 9.0

    phsyics_default = [[0, 0, 0], [0, 0, 0]]

    # sprite.add_particle(position=[1.0, 0, 0], physics=phsyics_default, fade=0 )
    # sprite.add_particle(position=[1.0, 0.25, 0], physics=phsyics_default, fade=0 )
    # sprite.add_particle(position=[1.0, 0.5, 0], physics=phsyics_default, fade=0 )
    # sprite.add_particle(position=[1.0, 0.75, 0], physics=phsyics_default, fade=0 )
    # sprite.add_particle(position=[1.0, 1.0, 0], physics=phsyics_default, fade=0 )
    # scene.run_for_time(step_time)

    max_x, max_y = scene.phys_size

    for _ in range( int(total_time/step_time) ):

        scene.run_for_time(step_time)

        if random() > 0.5:
            new_pos = [random() * max_x, random() * max_y, 0]
            #print(new_pos)
            sprite.add_particle(position=new_pos, physics=phsyics_default, fade=0.5 )

    scene.export_gif(r"c:/temp/govee.gif")
    