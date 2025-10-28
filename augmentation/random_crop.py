import random

def apply_random_crop(image, crop_width, crop_height):
    """Görüntüden rastgele bir bölgeyi keser."""
    h, w = image.shape[:2]
    if crop_height > h or crop_width > w:
        return image # Kırpma boyutu görüntüden büyükse orijinali döndür
    
    x = random.randint(0, w - crop_width)
    y = random.randint(0, h - crop_height)
    return image[y:y+crop_height, x:x+crop_width]