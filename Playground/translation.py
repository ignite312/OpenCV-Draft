# import cv2 as cv
# import numpy as np

# # Load image
# img = cv.imread('../Images/icpc.jpg', cv.IMREAD_COLOR)

# # Check if image loaded
# if img is None:
#     print("Error: Image not found")
#     exit()

# # Get image dimensions
# rows, cols = img.shape[:2]

# # -------------------------------
# # 1. Move Right (tx=100, ty=0)
# # -------------------------------
# M_right = np.float32([[1, 0, 100], [0, 1, 0]])
# right = cv.warpAffine(img, M_right, (cols, rows))

# # -------------------------------
# # 2. Move Down (tx=0, ty=50)
# # -------------------------------
# M_down = np.float32([[1, 0, 0], [0, 1, 50]])
# down = cv.warpAffine(img, M_down, (cols, rows))

# # -------------------------------
# # 3. Move Diagonally (tx=100, ty=50)
# # -------------------------------
# M_diag = np.float32([[1, 0, 100], [0, 1, 50]])
# diag = cv.warpAffine(img, M_diag, (cols, rows))

# # -------------------------------
# # 4. Move Left & Up (negative shift)
# # -------------------------------
# M_left_up = np.float32([[1, 0, -100], [0, 1, -50]])
# left_up = cv.warpAffine(img, M_left_up, (cols, rows))

# # -------------------------------
# # Show Results
# # -------------------------------
# cv.imshow("Original", img)
# cv.imshow("Right Shift", right)
# cv.imshow("Down Shift", down)
# cv.imshow("Diagonal Shift", diag)
# cv.imshow("Left Up Shift", left_up)

# cv.waitKey(0)
# cv.destroyAllWindows()


import cv2 as cv
import numpy as np

img = cv.imread('../Images/icpc.jpg', cv.IMREAD_COLOR)
rows, cols = img.shape[:2]

M = np.float32([[1, 0, 0], [0, -1, rows-1]])

# Same size
same = cv.warpAffine(img, M, (cols, rows))

# Bigger canvas
bigger = cv.warpAffine(img, M, (cols, rows))

# Smaller canvas
smaller = cv.warpAffine(img, M, (200, 200))

cv.imshow("Same Size", same)
cv.imshow("Bigger", bigger)
cv.imshow("Smaller", smaller)

cv.waitKey(0)
cv.destroyAllWindows()