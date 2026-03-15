import cv2

def load_image(path):
    img = cv2.imread(path)
    return img

def save_image(path, img):
    cv2.imwrite(path, img)