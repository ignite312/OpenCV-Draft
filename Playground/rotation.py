import cv2 as cv

# Load image
img = cv.imread('../Images/icpc.jpg', cv.IMREAD_COLOR)

# Get image dimensions
(h, w) = img.shape[:2]

# Find center of the image
center = (w // 2, h // 2)

# Create rotation matrix
M = cv.getRotationMatrix2D(center, 90, 0.5)

# Apply rotation
rotated = cv.warpAffine(img, M, (w, h))

# Show result
cv.imshow("Original", img)
cv.imshow("Rotated", rotated)

cv.waitKey(0)
cv.destroyAllWindows()