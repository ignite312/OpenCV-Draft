import cv2 as cv
# Load main image and logo
img = cv.imread("image.jpg")
logo = cv.imread("logo.png")

rows, cols, _ = logo.shape
roi = img[0:rows, 0:cols]

# Convert logo to grayscale and threshold
logo_gray = cv.cvtColor(logo, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(logo_gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)
cv.imshow("Mask", mask)
cv.imshow("Mask Inverse", mask_inv)
cv.imshow("Logo Grayscale", logo_gray)
# Black-out the ROI on the main image
img_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
cv.imshow("Image Background", img_bg)
# Take only the logo region
logo_fg = cv.bitwise_and(logo, logo, mask=mask)
cv.imshow("Logo Foreground", logo_fg)

# Put logo on ROI
dst = cv.add(img_bg, logo_fg)
img[0:rows, 0:cols] = dst

cv.imshow("Logo on Image", img)
cv.waitKey(0)
cv.destroyAllWindows()