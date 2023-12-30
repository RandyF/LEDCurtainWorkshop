from PIL import Image

# Example: Creating an image from raw byte data
width, height = 60, 26

# Example raw byte data (RGBA values, each ranging from 0 to 255)
framedat = [255, 255, 255, 255] * width * height
print( framedat )
raw_data = bytes(framedat)  # Replace r, g, b, a with your actual values
print(raw_data)

# Create an image from raw byte data
image = Image.frombytes("RGBA", (width, height), raw_data)

# Display or save the image as needed
image.show()