import cv2

def apply_color_space_transform(image, space):
    """Görüntüyü farklı bir renk uzayına dönüştürür."""
    if space == "HSV":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif space == "LAB":
        return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    elif space == "YCrCb":
        return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    return image