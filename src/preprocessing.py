import os
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import splitfolders
from PIL import Image
import io

# --------- Dataset Preparation ---------

def prepare_dataset_dataframe(base_path):
    data = []
    classes = os.listdir(base_path)
    for class_label in classes:
        class_path = os.path.join(base_path, class_label)
        if not os.path.isdir(class_path):
            continue
        for img_file in os.listdir(class_path):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                data.append({
                    'filepath': os.path.join(class_path, img_file),
                    'label': class_label
                })
    df = pd.DataFrame(data)
    return df

def split_dataset(input_folder, output_folder, ratio=(0.8, 0.1, 0.1), seed=42):
    if os.path.exists(output_folder) and os.listdir(output_folder):
        print(f"[INFO] Output folder '{output_folder}' exists and is not empty. Skipping split.")
    else:
        print(f"[INFO] Splitting dataset from '{input_folder}' into '{output_folder}' ...")
        splitfolders.ratio(input_folder, output=output_folder, seed=seed, ratio=ratio, group_prefix=None)
        print("[INFO] Split completed.")

def create_image_generators(train_dir, val_dir, test_dir, image_size=(128,128), batch_size=32, seed=42):
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        seed=seed
    )
    val_generator = val_test_datagen.flow_from_directory(
        val_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        seed=seed
    )
    test_generator = val_test_datagen.flow_from_directory(
        test_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        seed=seed
    )
    return train_generator, val_generator, test_generator

# --------- Preprocessing for Local Prediction (from file path) ---------

def preprocess_image_for_prediction(img_path, target_size=(128, 128)):
    img = load_img(img_path, target_size=target_size)
    x = img_to_array(img)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)
    return x


# --------- Preprocessing for API Uploads (from bytes) ---------

def preprocess_image(img_bytes, target_size=(128, 128)):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize(target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array


# --------- Main CLI Block ---------

if __name__ == "__main__":
    # Adjust paths to your project layout
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dataset_path = os.path.join(project_root, "dataset")
    output_dataset_path = os.path.join(base_dataset_path, "split_data")

    # Step 1: Prepare DataFrame (optional preview)
    df = prepare_dataset_dataframe(base_dataset_path)
    print("[INFO] Sample dataset entries:")
    print(df.sample(5))

    # Step 2: Split dataset only if not already split
    split_dataset(base_dataset_path, output_dataset_path)

    print("[INFO] Preprocessing complete.")
