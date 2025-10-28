import cv2

def apply_canny(image, threshold1, threshold2):
    """Canny kenar algılama algoritmasını uygular."""
    return cv2.Canny(image, threshold1, threshold2)