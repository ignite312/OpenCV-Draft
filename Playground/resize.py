import cv2 as cv

img = cv.imread('../Images/icpc.JPG')

# Different interpolations
nearest = cv.resize(img, None, fx=4, fy=4, interpolation=cv.INTER_NEAREST)
linear  = cv.resize(img, None, fx=4, fy=2, interpolation=cv.INTER_LINEAR)
cubic   = cv.resize(img, None, fx=4, fy=2, interpolation=cv.INTER_CUBIC)

cv.imshow("Nearest", nearest)
cv.imshow("Linear", linear)
cv.imshow("Cubic", cubic)

cv.waitKey(0)
cv.destroyAllWindows()