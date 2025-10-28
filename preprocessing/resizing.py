import cv2

def apply_resize(image, width, height):
    """Görüntüyü belirtilen genişlik ve yüksekliğe yeniden boyutlandırır."""
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)