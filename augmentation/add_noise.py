import numpy as np
import cv2 
def apply_gaussian_noise(image, std_dev):
    """Görüntüye Gaussian gürültüsü ekler."""
    mean = 0
    gauss = np.random.normal(mean, std_dev, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, gauss)
    return noisy_image