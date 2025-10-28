import cv2

def apply_crop(image, x, y, width, height):
    """
    Görüntüyü belirtilen başlangıç koordinatlarından (x, y) itibaren,
    verilen genişlik ve yükseklik değerlerine göre kırpar.

    Args:
        image (numpy.ndarray): Kırpılacak görüntü.
        x (int): Kırpma alanının sol üst köşesinin x koordinatı.
        y (int): Kırpma alanının sol üst köşesinin y koordinatı.
        width (int): Kırpma alanının genişliği.
        height (int): Kırpma alanının yüksekliği.

    Returns:
        numpy.ndarray: Kırpılmış görüntü.
    """
    # Görüntü boyutlarını kontrol ederek kırpma alanının dışarı taşmasını engelle
    h_img, w_img = image.shape[:2]
    
    # Başlangıç noktaları negatif olamaz
    x = max(0, x)
    y = max(0, y)
    
    # Bitiş noktaları görüntü boyutlarını aşamaz
    x_end = min(w_img, x + width)
    y_end = min(h_img, y + height)

    # NumPy'nin array slicing (dizi dilimleme) özelliği ile kırpma işlemi yapılır
    return image[y:y_end, x:x_end]