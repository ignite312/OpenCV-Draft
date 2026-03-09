import cv2 as cv
import numpy as np

# Read the image
image = cv.imread('bd.png')  # <-- replace with your image path

# Convert BGR to HSV
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

# ----------- RED COLOR RANGE -----------
# Red wraps around the Hue range, so two ranges are needed
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([179, 255, 255])

# Threshold the HSV image to get only red
mask1 = cv.inRange(hsv, lower_red1, upper_red1)
mask2 = cv.inRange(hsv, lower_red2, upper_red2)
mask_red = mask1 + mask2

# Optional: remove noise
kernel = np.ones((5, 5), np.uint8)
mask_red = cv.morphologyEx(mask_red, cv.MORPH_OPEN, kernel)
mask_red = cv.morphologyEx(mask_red, cv.MORPH_CLOSE, kernel)

# Extract the red color from the original image
result = cv.bitwise_and(image, image, mask=mask_red)

# Show the images
cv.imshow("Original Image", image)
cv.imshow("Red Mask", mask_red)
cv.imshow("Tracked Red Color", result)

cv.waitKey(0)
cv.destroyAllWindows()