Image_Processor_App/
├── main_app.py              # Ana arayüzü ve orkestrasyonu içeren dosya
│
├── preprocessing/           # Ön işleme modüllerinin bulunduğu klasör
│   ├── __init__.py          # Bu klasörün bir Python paketi olduğunu belirtir (boş dosya)
│   ├── resizing.py
│   ├── grayscale.py
│   ├── histogram_equalization.py
│   ├── denoising.py
│   ├── cropping.py
│   ├── edge_detection.py
│   └── color_space.py
│
└── augmentation/            # Veri artırma modüllerinin bulunduğu klasör
    ├── __init__.py          # (Boş dosya)
    ├── rotation.py
    ├── flipping.py
    ├── translation.py
    ├── zooming.py
    ├── random_crop.py
    ├── brightness_contrast.py
    ├── add_noise.py
    └── cutout.py


<<<<<<<<<<<<<<<<<<<<Kullanım<<<<<<<<<<<<<<<<<<

<Kaynak ve hedef klasörleri seçin.

<İşlem akışını oluşturun:

<Sol panelden bir işlem seçin ve tıklayın → pipeline’a eklenir.

<Sağ panelde seçilen işlemin parametrelerini düzenleyin.

<İşlemleri sıralamak ve silmek için pipeline listesini kullanın.

<Veri artırma adedini belirleyin (opsiyonel, yalnızca augmentation işlemleri için geçerli).

<Toplu işlem başlatın: “Tümünü İşle ve Kaydet” butonuna basın.

<İşlem tamamlandığında hedef klasörde işlenmiş resimleri bulabilirsiniz.

<<<<<<<<<<<<<<<<Örnek Kullanım<<<<<<<<<<<<<<<<<<

<Resize ve Grayscale

<“Resize” ekle, w=512, h=512

<“Grayscale” ekle

<“Tümünü İşle ve Kaydet”

<Veri Artırma Örneği

<“Rotation” ekle, angle=15

<“Flipping” ekle

<Oluşturulacak resim adedini 5 yapın

<“Tümünü İşle ve Kaydet”
