import cv2
import numpy as np
from PIL import Image, ImageOps
from rembg import remove


def adjust_brightness(img, value): # Adjust brightness by adding a constant value to all pixels
    return cv2.convertScaleAbs(img, alpha=1, beta=value)

def adjust_contrast(img, alpha=1.0): # Adjust contrast by multiplying all pixel values by a constant factor
    return cv2.convertScaleAbs(img, alpha=alpha, beta=0)

def rotate(img, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
    return cv2.warpAffine(img, M, (w, h))

def process_gray_background(cv_image):
    cv_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv_rgb).convert("RGBA")

    # Remove background 
    mask_image = remove(pil_img)

    alpha_mask = mask_image.split()[-1]
    gray_bg = ImageOps.grayscale(pil_img).convert("RGBA")
    final_pil = Image.composite(pil_img, gray_bg, alpha_mask)
    final_cv = cv2.cvtColor(np.array(final_pil), cv2.COLOR_RGBA2BGR)

    return final_cv