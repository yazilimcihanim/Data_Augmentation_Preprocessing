import cv2

def apply_median_blur(image, kernel_size):
    """Median blur filtresi ile gürültü azaltma uygular."""
    # Kernel boyutu tek sayı olmalıdır
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.medianBlur(image, kernel_size)