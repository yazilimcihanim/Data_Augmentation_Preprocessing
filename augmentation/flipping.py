import cv2
import random

def apply_flip(image):
    """Görüntüyü rastgele yatay veya dikey olarak çevirir."""
    flip_code = random.choice([0, 1]) # 0: Dikey, 1: Yatay
    return cv2.flip(image, flip_code)