import os
import numpy as np
from PIL import Image

# --- 🔧 CONFIGURA AQUÍ TU RUTA BASE ---
BASE_DIR = r"C:\Users\alems\Downloads\ADA\pca"

# --- 📂 RUTAS DE GALERÍA Y PRUEBA ---
GALLERY = os.path.join(BASE_DIR, "Gallery", "Gallery")
PROBE = os.path.join(BASE_DIR, "Probe", "Probe")

# --- 📸 CARGA DE IMÁGENES ---
def load_images_from_folder(folder_path):
    images = []
    labels = []

    # Recorre cada subcarpeta (s1, s2, ..., s40)
    for folder in os.listdir(folder_path):
        folder_full = os.path.join(folder_path, folder)

        # Saltar si no es una carpeta válida
        if not os.path.isdir(folder_full):
            continue

        for img_name in os.listdir(folder_full):
            img_path = os.path.join(folder_full, img_name)
            try:
                img = Image.open(img_path).convert("L")  # convertir a escala de grises
                images.append(np.array(img))
                # obtiene el número después de la 's' (ej: 's12' → 12)
                labels.append(int(folder.split("s")[1]))
            except Exception as e:
                print(f"⚠️ Error cargando {img_path}: {e}")

    print(f"✅ Se cargaron {len(images)} imágenes desde {folder_path}")
    return images, labels


# --- 🚀 CARGAR GALERÍA Y PRUEBA ---
gallery_images, gallery_labels = load_images_from_folder(GALLERY)
probe_images, probe_labels = load_images_from_folder(PROBE)

# --- 🧩 VERIFICACIÓN RÁPIDA ---
print(f"Total imágenes en Gallery: {len(gallery_images)}")
print(f"Total imágenes en Probe: {len(probe_images)}")
print(f"Tamaño de una imagen: {gallery_images[0].shape}")
