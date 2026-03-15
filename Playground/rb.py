from rembg import remove
from PIL import Image, ImageOps
import numpy as np

# Load the input image
input_image = Image.open("f.jpg").convert("RGBA")

# Get the alpha mask from rembg (background removed)
mask_image = remove(input_image)

# Convert mask to grayscale (just the alpha channel)
mask = mask_image.split()[-1]  # alpha channel as mask

# Convert original image to grayscale
gray_bg = ImageOps.grayscale(input_image).convert("RGBA")

# Combine grayscale background and original color foreground using the mask
final_image = Image.composite(input_image, gray_bg, mask)

# Save result
final_image.save("output.png")