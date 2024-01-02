from PIL import Image

def gif_to_frames(gif_path):
    # Open the GIF file
    gif_image = Image.open(gif_path)

    # Extract frames
    frames = []
    for frame in range(gif_image.n_frames):
        gif_image.seek(frame)
        rgba_frame = gif_image.convert("RGBA")

        # Convert to a 2D array of [r, g, b, a] values
        frame_data = list(rgba_frame.getdata())
        frame_array = [list(pixel) for pixel in frame_data]

        frames.append(frame_array)

    return frames


#--------------------------------------------------------------------------
# Calculate "complexity" as the number of changes between frames.
# I think this is the ulitmate limitation for Govee Imports
#--------------------------------------------------------------------------
def calc_frame_complexity(frame_a, frame_b):

    cplx = 0

    for y, element in enumerate(frame_a):
            if element != frame_b[y]:
                cplx += 1
    
    return cplx


def stack_complexity(raw_frames):

    complxity = len(raw_frames[0][0])

    for i, frame in enumerate(raw_frames):
        if i > 0:
            complxity += calc_frame_complexity( raw_frames[i-1], raw_frames[i] )

    return complxity

def get_gif_complexity(gif_path):
     
    frames = gif_to_frames(gif_path)

    # Print the first frame's pixel values
    return stack_complexity(frames)


#     def create_check(self, c1, c2):
        
#         ctr = 0
#         tFrame = []
#         for col in range(self.px_height):
#             tRow = []
#             for row in  range(self.px_width):
#                 if ctr % 2:
#                     tRow.append( c1 )
#                 else:
#                     tRow.append( c2 )
#                 ctr += 1
#             tFrame.append( tRow )
#             if not self.px_width % 2:
#                 ctr += 1
        
#         return tFrame

#     def create_noise(self):
        
#         tFrame = []
#         for col in range(self.px_height):
#             tRow = []
#             for row in  range(self.px_width):
#                 tRow.append( [randint(0, 255), randint(0, 255), randint(0, 255), 255] )
#             tFrame.append( tRow )
        
#         return tFrame
                        


#     def complexity_research(self, cplx_limit=None):

#         for _ in range(4):

# #            frame_pixels = self.create_check([randint(0, 255), randint(0, 255), randint(0, 255), 255], [randint(0, 255), randint(0, 255), randint(0, 255), 255])
#             frame_pixels = self.create_noise()
#             self.raw_frames.append(frame_pixels)


#         self.export_gif(r"c:/temp/govee_cplx.gif", cplx_limit=cplx_limit)
        



if __name__ == "__main__":

    print(get_gif_complexity(r"c:/temp/govee_001.gif"))