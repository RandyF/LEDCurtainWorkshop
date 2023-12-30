from PIL import Image


class CurtainScene:

    sprites = []


    def create_animated_gif(frames, output_path, duration=100, loop=0):
        # Create an Image object with the specified size
        width, height = 60, 26
        image = Image.new("RGBA", (width, height))

        # Save each frame as a separate image
        images = []
        for frame_data in frames:
            frame = Image.frombytes("RGBA", (width, height), frame_data)
            images.append(frame)

        # Save the animated GIF
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop,
        )

    # Example usage:
    # frames is a list of RGBA frames (e.g., [(r1, g1, b1, a1), (r2, g2, b2, a2), ...])
    # output_path is the file path where the animated GIF will be saved
    # duration is the duration of each frame in milliseconds
    # loop is the number of loops (0 for infinite loop)
    # create_animated_gif(frames, output_path, duration=100, loop=0)


if __name__ == "__main__":
    print("Curtain Scene Test")