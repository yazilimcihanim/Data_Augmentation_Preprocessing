import cv2
import random

def apply_rotation(image, max_angle):
    """Görüntüyü rastgele bir açıyla döndürür."""
    angle = random.uniform(-max_angle, max_angle)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REFLECT_101)