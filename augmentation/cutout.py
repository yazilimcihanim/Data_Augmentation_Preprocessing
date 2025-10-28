import numpy as np
import random

def apply_cutout(image, num_holes, max_hole_size):
    """Görüntü üzerine rastgele siyah kareler (cutout) ekler."""
    img = image.copy()
    h, w = img.shape[:2]
    
    for _ in range(num_holes):
        hole_h = random.randint(1, max_hole_size)
        hole_w = random.randint(1, max_hole_size)
        
        y1 = np.clip(random.randint(0, h - hole_h), 0, h)
        x1 = np.clip(random.randint(0, w - hole_w), 0, w)
        y2 = y1 + hole_h
        x2 = x1 + hole_w
        
        img[y1:y2, x1:x2] = 0 # Siyah renk
        
    return img