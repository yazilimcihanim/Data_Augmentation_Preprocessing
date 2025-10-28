import cv2

def apply_grayscale(image):
    """Görüntüyü gri tonlamalı hale getirir."""
    # Eğer görüntü zaten tek kanallı değilse dönüştür
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image