import cv2
import random

def apply_zoom(image, max_zoom_factor):
    """Görüntüye rastgele yakınlaştırma veya uzaklaştırma uygular."""
    factor = random.uniform(1 - max_zoom_factor, 1 + max_zoom_factor)
    h, w = image.shape[:2]
    new_h, new_w = int(h * factor), int(w * factor)
    
    if factor < 1: # Uzaklaştırma
        zoomed = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        pad_h = (h - new_h) // 2
        pad_w = (w - new_w) // 2
        return cv2.copyMakeBorder(zoomed, pad_h, h - new_h - pad_h, pad_w, w - new_w - pad_w, cv2.BORDER_CONSTANT, value=[0,0,0])
    else: # Yakınlaştırma
        zoomed = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        crop_h = (new_h - h) // 2
        crop_w = (new_w - w) // 2
        return zoomed[crop_h:crop_h + h, crop_w:crop_w + w]