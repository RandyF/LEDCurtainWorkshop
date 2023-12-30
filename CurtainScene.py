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
#
#==============================================================================

#==============================================================================
# Package Includes
#==============================================================================
from PIL import Image
#import numpy as np


#==============================================================================
# Project Includes
#==============================================================================
from CurtainSprite import CurtainSprite
from CurtainParticle import CurtainParticle


#==============================================================================
# Curtain Scene Class
# Manages Sprites and Renders Images
#==============================================================================
class CurtainScene:

    width, height = 60, 26
    time_step_s = 0.200

    sprites = []

    frames = []


    #--------------------------------------------------------------------------
    # Render the Current Frame
    #--------------------------------------------------------------------------
    def render_frame(self):
        print("render_frame")

        frame_pixels = [ [[0, 0, 0, 255]] * self.width for _ in range(self.height)]

        for sprite in self.sprites:
            pixels = sprite.pixelize()

            for (pos_x, pos_y, pos_z), (c_r, c_g, c_b, c_a) in pixels:

                #print( (pos_x, pos_y, pos_z), (c_r, c_g, c_b, c_a) )

                cur_y = self.height-1-pos_y
                cur_x = pos_x
                #print(cur_x, cur_y)

                cur_r, cur_g, cur_b, cur_a = frame_pixels[cur_y][cur_x]
                #print(cur_r, cur_g, cur_b, cur_a)

                cur_r = c_r  # TODO: alpha
                cur_g = c_g  # TODO: alpha
                cur_b = c_b  # TODO: alpha

                #print(cur_r, cur_g, cur_b)

                frame_pixels[cur_y][cur_x] = [cur_r, cur_g, cur_b, 0]


        #fully unroll the frame
        framedat = [element for row in [element for row in frame_pixels for element in row] for element in row]
                
        frame_image = Image.frombytes("RGBA", (self.width, self.height), bytes(framedat) )

        self.frames.append(frame_image)



    #--------------------------------------------------------------------------
    # Export the current frame image array as a gif
    #--------------------------------------------------------------------------
    def export_gif(self, output_path, duration=time_step_s*1000, loop=0):

        # Save the animated GIF
        self.frames[0].save(
            output_path,
            save_all=True,
            append_images=self.frames[1:],
            duration=duration,
            loop=loop,
        )



#==============================================================================
# Stand-Alone Runtime
#==============================================================================
if __name__ == "__main__":
    print("Curtain Scene Test")

    scene = CurtainScene()

    sprite = CurtainSprite()

    part = CurtainParticle(0, 0)
    sprite.particles.append(part)
    part = CurtainParticle(59, 25)
    sprite.particles.append(part)

    scene.sprites.append( sprite )

    scene.render_frame()

    scene.export_gif(r"c:/temp/govee.gif")
    