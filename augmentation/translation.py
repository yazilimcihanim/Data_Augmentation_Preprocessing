import cv2
import numpy as np
import random

def apply_translation(image, max_x_shift, max_y_shift):
    """Görüntüyü yatay ve dikey eksenlerde rastgele öteler."""
    h, w = image.shape[:2]
    tx = random.uniform(-max_x_shift, max_x_shift) * w
    ty = random.uniform(-max_y_shift, max_y_shift) * h
    translation_matrix = np.array([[1, 0, tx], [0, 1, ty]], dtype=np.float32)
    return cv2.warpAffine(image, translation_matrix, (w, h))