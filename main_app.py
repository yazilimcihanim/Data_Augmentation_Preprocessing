import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, cv2, copy, random, traceback
import ttkbootstrap as bst
from PIL import Image, ImageTk

# --- MODÜLLERİ İÇERİ AKTARMA ---
# (Modüllerin projenizde doğru yollarda olduğundan emin olun)
from preprocessing.resizing import apply_resize
from preprocessing.grayscale import apply_grayscale
from preprocessing.histogram_equalization import apply_hist_equalization
from preprocessing.denoising import apply_median_blur
from preprocessing.cropping import apply_crop
from preprocessing.edge_detection import apply_canny
from preprocessing.color_space import apply_color_space_transform

from augmentation.rotation import apply_rotation
from augmentation.flipping import apply_flip
from augmentation.translation import apply_translation
from augmentation.zooming import apply_zoom
from augmentation.random_crop import apply_random_crop
from augmentation.brightness_contrast import apply_brightness_contrast
from augmentation.add_noise import apply_gaussian_noise
from augmentation.cutout import apply_cutout


class AdvancedImageProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Görüntü İşleme Arayüzü")
        self.root.geometry("1400x900")

        # Durum ve pipeline
        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.original_cv_image = None
        self.preview_cv_image = None
        self.pipeline = []
        self.num_augment_var = tk.StringVar(value="5")

        # Operasyon tanımları ve fonksiyon haritası
        self.operations_config = self._setup_operations()
        self.function_map = self._setup_function_map()

        # Ana çerçeve
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(1, weight=3) # Görüntü alanı
        main_frame.rowconfigure(2, weight=2) # Kontrol alanı
        main_frame.columnconfigure(0, weight=1)

        self.create_io_widgets(main_frame)

        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(0, weight=1)
        self.create_image_panels(image_frame)

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=2)
        control_frame.rowconfigure(0, weight=1)

        self.create_operation_library_panel(control_frame)
        self.create_pipeline_panel(control_frame)
        self.create_parameter_panel(control_frame)
        self.create_augmentation_controls(control_frame)
        self.create_action_widgets(main_frame)

    # --- OPERASYON VE FONKSİYON HARİTASI ---
    def _setup_operations(self):
        return {
            "Resize": {"category": "prep", "params": {"w": tk.StringVar(value="512"), "h": tk.StringVar(value="512")}},
            "Crop": {"category": "prep", "params": {"x": tk.StringVar(value="0"), "y": tk.StringVar(value="0"), "w": tk.StringVar(value="256"), "h": tk.StringVar(value="256")}},
            "Grayscale": {"category": "prep", "params": {}},
            "Histogram Equalization": {"category": "prep", "params": {}},
            "Denoise (Median)": {"category": "prep", "params": {"ksize": tk.StringVar(value="5")}},
            "Edge Detection (Canny)": {"category": "prep", "params": {"t1": tk.StringVar(value="100"), "t2": tk.StringVar(value="200")}},
            "Color Space": {"category": "prep", "params": {"space": tk.StringVar(value="HSV")}},
            "Rotation": {"category": "aug", "params": {"angle": tk.StringVar(value="15")}},
            "Flipping": {"category": "aug", "params": {}},
            "Translation": {"category": "aug", "params": {"x_shift": tk.StringVar(value="0.1"), "y_shift": tk.StringVar(value="0.1")}},
            "Zoom": {"category": "aug", "params": {"factor": tk.StringVar(value="0.2")}},
            "Random Crop": {"category": "aug", "params": {"w": tk.StringVar(value="450"), "h": tk.StringVar(value="450")}},
            "Brightness/Contrast": {"category": "aug", "params": {"bright": tk.StringVar(value="20"), "contrast": tk.StringVar(value="0.2")}},
            "Gaussian Noise": {"category": "aug", "params": {"std_dev": tk.StringVar(value="10")}},
            "Cutout": {"category": "aug", "params": {"holes": tk.StringVar(value="3"), "size": tk.StringVar(value="40")}}
        }

    def _setup_function_map(self):
        return {
            "Resize": apply_resize, "Crop": apply_crop, "Grayscale": apply_grayscale,
            "Histogram Equalization": apply_hist_equalization, "Denoise (Median)": apply_median_blur,
            "Edge Detection (Canny)": apply_canny, "Color Space": apply_color_space_transform,
            "Rotation": apply_rotation, "Flipping": apply_flip, "Translation": apply_translation,
            "Zoom": apply_zoom, "Random Crop": apply_random_crop,
            "Brightness/Contrast": apply_brightness_contrast, "Gaussian Noise": apply_gaussian_noise,
            "Cutout": apply_cutout,
        }

    # --- ARAYÜZ OLUŞTURMA ---
    def create_io_widgets(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.grid(row=0, column=0, sticky="ew")

        io_frame = ttk.LabelFrame(top_frame, text="Dosya Yolları", padding=10)
        io_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        io_frame.columnconfigure(1, weight=1)

        ttk.Label(io_frame, text="Kaynak Klasör:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(io_frame, textvariable=self.input_folder_path, state='readonly').grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(io_frame, text="Gözat", command=self._select_input_folder, bootstyle="outline").grid(row=0, column=2)
        ttk.Label(io_frame, text="Hedef Klasör:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(io_frame, textvariable=self.output_folder_path, state='readonly').grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Button(io_frame, text="Gözat", command=lambda: self.output_folder_path.set(filedialog.askdirectory() or self.output_folder_path.get()), bootstyle="outline").grid(row=1, column=2)

        theme_frame = ttk.LabelFrame(top_frame, text="Görünüm Ayarları", padding=10)
        theme_frame.pack(side=tk.RIGHT, fill=tk.X, padx=10)
        
        ttk.Label(theme_frame, text="Tema:").pack(side=tk.LEFT, padx=(0,5))
        self.theme_combobox = ttk.Combobox(theme_frame, state="readonly", values=self.root.style.theme_names())
        
        # DÜZELTİLDİ: .theme.name kullanılıyor
        self.theme_combobox.set(self.root.style.theme.name)
        
        self.theme_combobox.pack(side=tk.LEFT)
        self.theme_combobox.bind("<<ComboboxSelected>>", self._change_theme)


    def create_operation_library_panel(self, parent):
        frame = ttk.LabelFrame(parent, text="Operasyon Kütüphanesi (Eklemek için tıkla)", padding=10)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.ops_tree = ttk.Treeview(frame, show="tree")
        
        prep_id = self.ops_tree.insert("", "end", text="Ön İşleme (Preprocessing)", open=False)
        aug_id = self.ops_tree.insert("", "end", text="Veri Artırma (Augmentation)", open=False)

        for name, config in self.operations_config.items():
            parent_id = prep_id if config["category"] == "prep" else aug_id
            self.ops_tree.insert(parent_id, "end", text=name, values=[name])

        self.ops_tree.grid(row=0, column=0, sticky="nsew")
        self.ops_tree.bind("<<TreeviewSelect>>", self._add_to_pipeline)

    def _select_input_folder(self, *args):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_path.set(folder)
            self._load_preview_image()

    def create_image_panels(self, parent, *args):
        original_frame = ttk.LabelFrame(parent, text="Orijinal Görüntü", padding=5)
        original_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.original_panel = ttk.Label(original_frame, anchor="center")
        self.original_panel.pack(fill=tk.BOTH, expand=True)

        preview_frame = ttk.LabelFrame(parent, text="Önizleme", padding=5)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        self.preview_panel = ttk.Label(preview_frame, anchor="center")
        self.preview_panel.pack(fill=tk.BOTH, expand=True)

    def create_pipeline_panel(self, parent, *args):
        frame = ttk.LabelFrame(parent, text="Aktif İşlem Akışı (Kaldırmak için tıkla)", padding=10)
        frame.grid(row=0, column=1, sticky="nsew", padx=5)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.pipeline_listbox = tk.Listbox(frame, exportselection=False)
        self.pipeline_listbox.grid(row=0, column=0, sticky="nsew")
        self.pipeline_listbox.bind("<<ListboxSelect>>", self._on_pipeline_select)
        self.pipeline_listbox.bind("<ButtonRelease-1>", self._remove_from_pipeline)

    def create_parameter_panel(self, parent, *args):
        self.param_frame = ttk.LabelFrame(parent, text="Parametreler", padding=10)
        self.param_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(5, 0))
        self.param_frame_label = ttk.Label(self.param_frame, text="Düzenlemek için aktif akıştan bir işlem seçin.", anchor="center")
        self.param_frame_label.pack(fill=tk.BOTH, expand=True)

    def create_augmentation_controls(self, parent, *args):
        frame = ttk.LabelFrame(parent, text="Veri Artırma Ayarları", padding=10)
        frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 5), pady=(10,0))
        
        ttk.Label(frame, text="Oluşturulacak Resim Adedi:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame, textvariable=self.num_augment_var, width=10).pack(side=tk.LEFT)

    def create_action_widgets(self, parent, *args):
        frame = ttk.LabelFrame(parent, text="Toplu İşlem", padding=10)
        frame.grid(row=3, column=0, sticky="ew", pady=(10,0))
        action_subframe = ttk.Frame(frame)
        action_subframe.pack(fill=tk.X, expand=True)
        self.progress_bar = ttk.Progressbar(action_subframe, mode='determinate', bootstyle="success-striped")
        self.progress_bar.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 10))
        self.start_button = ttk.Button(action_subframe, text="Tümünü İşle ve Kaydet", command=self.process_all_images, bootstyle="success")
        self.start_button.pack(side=tk.RIGHT)
        
        self.status_label = ttk.Label(parent, text="Durum: Bekleniyor...")
        self.status_label.grid(row=4, column=0, sticky="w", padx=10, pady=(5,0))


    # --- OLAY YÖNETİMİ VE MANTIK ---
    
    def _change_theme(self, event=None):
        selected_theme = self.theme_combobox.get()
        self.root.style.theme_use(selected_theme)
        self.status_label.config(text=f"Tema '{selected_theme}' olarak değiştirildi.")


    def _load_preview_image(self, *args):
        in_path = self.input_folder_path.get()
        if not in_path or not os.path.isdir(in_path): return
        image_files = [f for f in os.listdir(in_path) if f.lower().endswith(('.png','.jpg','.jpeg'))]
        if not image_files: return
        file_path = os.path.join(in_path, random.choice(image_files))
        img = cv2.imread(file_path)
        if img is None: return
        self.original_cv_image = img
        self.preview_cv_image = img.copy()
        self._update_display_image(self.original_panel, self.original_cv_image)
        self._update_preview()
        self.status_label.config(text=f"Durum: Önizleme için {os.path.basename(file_path)} yüklendi.")


    def _add_to_pipeline(self, event=None):
        selected_id = self.ops_tree.focus()
        if not selected_id or not self.ops_tree.parent(selected_id):
            return
            
        op_name = self.ops_tree.item(selected_id, "values")[0]
        
        new_params = {key: tk.StringVar(value=var.get()) for key, var in self.operations_config[op_name]["params"].items()}
        new_op_instance = {"name": op_name, "params": new_params}
        
        self.pipeline.append(new_op_instance)
        self.pipeline_listbox.insert(tk.END, op_name)
        
        self.pipeline_listbox.selection_clear(0, tk.END)
        self.pipeline_listbox.selection_set(tk.END)
        self._on_pipeline_select()
        self._update_preview()

    def _remove_from_pipeline(self, event=None):
        selected_indices = self.pipeline_listbox.curselection()
        if not selected_indices: return
        idx = selected_indices[0]
        
        self.pipeline.pop(idx)
        self.pipeline_listbox.delete(idx)
        
        self._populate_parameter_panel(None)
        
        if self.pipeline_listbox.size() > 0:
            new_selection = max(0, idx - 1)
            self.pipeline_listbox.selection_set(new_selection)
            self._on_pipeline_select()
        self._update_preview()

    def _on_pipeline_select(self, event=None):
        selected_indices = self.pipeline_listbox.curselection()
        if not selected_indices: 
            self._populate_parameter_panel(None)
            return
        pipeline_item = self.pipeline[selected_indices[0]]
        self._populate_parameter_panel(pipeline_item)

    def _populate_parameter_panel(self, pipeline_item):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        if pipeline_item is None:
            self.param_frame_label = ttk.Label(self.param_frame, text="Düzenlemek için aktif akıştan bir işlem seçin.", anchor="center")
            self.param_frame_label.pack(fill=tk.BOTH, expand=True)
            self.param_frame.config(text="Parametreler")
            return
        
        self.param_frame.config(text=f"Parametreler: {pipeline_item['name']}")
        if not pipeline_item["params"]:
            ttk.Label(self.param_frame, text="Bu işlem için parametre yok.", anchor="center").pack(pady=10, padx=5)
            return

        for param_name, param_var in pipeline_item["params"].items():
            param_var.trace_add("write", self._on_param_change)
            row = ttk.Frame(self.param_frame)
            row.pack(fill=tk.X, pady=2, padx=5)
            ttk.Label(row, text=f"{param_name.capitalize()}:", width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(row, textvariable=param_var)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _on_param_change(self, *args):
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(250, self._update_preview)

    def _update_preview(self):
        if self.preview_cv_image is None: return
        processed_image = self._apply_pipeline_to_image(self.preview_cv_image.copy())
        self._update_display_image(self.preview_panel, processed_image)

    def _update_display_image(self, panel, cv_image):
        if cv_image is None: return
        panel_w, panel_h = panel.winfo_width(), panel.winfo_height()
        if panel_w < 50 or panel_h < 50: panel_w, panel_h = 600, 400
        
        img_h, img_w = cv_image.shape[:2]
        
        # DÜZELTİLDİ: En-boy oranı doğru hesaplanıyor (hata img_w / img_w idi)
        if img_h == 0: return # Sıfıra bölme hatasını engelle
        aspect_ratio = img_w / img_h
        
        new_w = panel_w
        new_h = int(new_w / aspect_ratio)
        if new_h > panel_h:
            new_h = panel_h
            new_w = int(new_h * aspect_ratio)

        # Genişlik veya yükseklik sıfırsa yeniden boyutlandırmayı atla
        if new_w <= 0 or new_h <= 0: return
        
        resized_img = cv2.resize(cv_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        if len(resized_img.shape) == 3:
            img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_GRAY2RGB)
            
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        panel.config(image=img_tk)
        panel.image = img_tk

    def _get_params_from_pipeline_item(self, pipeline_item):
        params = {}
        for k, v in pipeline_item["params"].items():
            val = v.get()
            try: 
                if '.' in val: params[k] = float(val)
                else: params[k] = int(val)
            except (ValueError, TypeError):
                params[k] = val
        return params

    def _apply_pipeline_to_image(self, image):
        temp_image = image
        for op_item in self.pipeline:
            temp_image = self._apply_single_op(temp_image, op_item)
        return temp_image

    def _apply_single_op(self, image, op_item):
        op_name = op_item["name"]
        op_func = self.function_map.get(op_name)
        if not op_func: return image
        p = self._get_params_from_pipeline_item(op_item)
        try:
            if op_name in ["Resize", "Random Crop"]: return op_func(image, p['w'], p['h'])
            elif op_name == "Crop": return op_func(image, p['x'], p['y'], p['w'], p['h'])
            elif op_name == "Denoise (Median)": return op_func(image, p['ksize'])
            elif op_name == "Edge Detection (Canny)":
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape)==3 else image
                return op_func(gray, p['t1'], p['t2'])
            elif op_name == "Color Space": return op_func(image, p['space'])
            elif op_name == "Rotation": return op_func(image, p['angle'])
            elif op_name == "Translation": return op_func(image, p['x_shift'], p['y_shift'])
            elif op_name == "Zoom": return op_func(image, p['factor'])
            elif op_name == "Brightness/Contrast": return op_func(image, p['bright'], p['contrast'])
            elif op_name == "Gaussian Noise": return op_func(image, p['std_dev'])
            elif op_name == "Cutout": return op_func(image, p['holes'], p['size'])
            else: return op_func(image)
        except Exception as e:
            self.status_label.config(text=f"Hata: {op_name} uygulanamadı - {e}")
            print(f"Hata: {op_name} uygulanamadı - {e}\n{traceback.format_exc()}")
            return image

    def process_all_images(self, *args):
        in_path = self.input_folder_path.get()
        out_path = self.output_folder_path.get()

        if not in_path or not out_path:
            messagebox.showerror("Hata", "Lütfen kaynak ve hedef klasörleri seçin.")
            return
        if not self.pipeline:
            messagebox.showwarning("Uyarı", "İşlem akışı boş. Lütfen en az bir operasyon ekleyin.")
            return
        if not os.path.isdir(out_path):
            try:
                os.makedirs(out_path)
            except OSError as e:
                messagebox.showerror("Hata", f"Hedef klasör oluşturulamadı: {e}")
                return
        
        try:
            num_augment = int(self.num_augment_var.get())
        except ValueError:
            messagebox.showerror("Hata", "Veri artırma sayısı geçerli bir tam sayı olmalıdır.")
            return

        self.start_button.config(state=tk.DISABLED)
        image_files = [f for f in os.listdir(in_path) if f.lower().endswith(('.png','.jpg','.jpeg'))]
        if not image_files:
            messagebox.showinfo("Bilgi", "Kaynak klasörde işlenecek resim bulunamadı.")
            self.start_button.config(state=tk.NORMAL)
            return

        self.progress_bar['maximum'] = len(image_files)
        
        prep_pipeline = [op for op in self.pipeline if self.operations_config[op['name']]['category'] == 'prep']
        aug_pipeline = [op for op in self.pipeline if self.operations_config[op['name']]['category'] == 'aug']

        try:
            for i, filename in enumerate(image_files):
                self.status_label.config(text=f"İşleniyor: {filename} ({i+1}/{len(image_files)})")
                self.progress_bar['value'] = i + 1
                self.root.update_idletasks()

                file_path = os.path.join(in_path, filename)
                current_image = cv2.imread(file_path)
                if current_image is None:
                    print(f"Uyarı: {filename} okunamadı, atlanıyor.")
                    continue

                preprocessed_image = current_image
                for op_item in prep_pipeline:
                    preprocessed_image = self._apply_single_op(preprocessed_image, op_item)

                base_name, ext = os.path.splitext(filename)
                
                if not aug_pipeline or num_augment == 0:
                    save_path = os.path.join(out_path, f"{base_name}_processed{ext}")
                    cv2.imwrite(save_path, preprocessed_image)
                else:
                    for j in range(num_augment):
                        augmented_image = preprocessed_image.copy()
                        for op_item in aug_pipeline:
                            augmented_image = self._apply_single_op(augmented_image, op_item)
                        
                        save_path = os.path.join(out_path, f"{base_name}_aug_{j+1}{ext}")
                        cv2.imwrite(save_path, augmented_image)

        except Exception as e:
            messagebox.showerror("İşlem Hatası", f"Toplu işleme sırasında bir hata oluştu: {e}\n\nDetaylar için konsolu kontrol edin.")
            print(traceback.format_exc())
        finally:
            self.status_label.config(text=f"Durum: İşlem tamamlandı. {len(image_files)} resim işlendi.")
            self.progress_bar['value'] = 0
            self.start_button.config(state=tk.NORMAL)
            messagebox.showinfo("Başarılı", "Tüm resimler başarıyla işlendi ve kaydedildi.")


if __name__ == "__main__":
    root = bst.Window(themename="superhero")
    app = AdvancedImageProcessorGUI(root)
    root.mainloop()