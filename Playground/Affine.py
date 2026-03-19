import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Read image
img = cv.imread('sudoku.png')

# Check if image loaded
assert img is not None, "file could not be read, check with os.path.exists()"

# Convert BGR → RGB (important for matplotlib)
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# Get shape
rows, cols, ch = img.shape

# Source points (from original image)
pts1 = np.float32([
    [56, 65],
    [368, 52],
    [28, 387],
    [389, 390]
])

# Destination points (where to map)
pts2 = np.float32([
    [0, 0],
    [300, 0],
    [0, 300],
    [300, 300]
])

# Perspective transformation matrix
M = cv.getPerspectiveTransform(pts1, pts2)

# Apply transformation
dst = cv.warpPerspective(img_rgb, M, (300, 300))

# Show images
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(img_rgb)
plt.title('Input')
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(dst)
plt.title('Output')
plt.axis('off')

plt.show()