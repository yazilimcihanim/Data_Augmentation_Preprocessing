import cv2
import numpy as np
import random

def apply_brightness_contrast(image, max_brightness_delta, max_contrast_delta):
    """Görüntünün parlaklığını ve kontrastını rastgele ayarlar."""
    brightness = random.uniform(-max_brightness_delta, max_brightness_delta)
    contrast = 1.0 + random.uniform(-max_contrast_delta, max_contrast_delta)
    
    # alpha (kontrast) ve beta (parlaklık) için formül
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)