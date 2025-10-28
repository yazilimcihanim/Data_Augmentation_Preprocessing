import cv2

def apply_hist_equalization(image):
    """Görüntünün kontrastını histogram eşitleme ile artırır."""
    if len(image.shape) == 3: # Renkli görüntü ise
        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else: # Gri görüntü ise
        return cv2.equalizeHist(image)