import os
import shutil
import time
from datetime import datetime
import traceback
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from dotenv import load_dotenv
from supabase import create_client, Client

from prediction import predict_image

import uuid
import zipfile
import aiofiles
from PIL import Image
import numpy as np

# TensorFlow imports for retrain
import tensorflow as tf
from keras.models import load_model, Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Dropout, Flatten, Dense
from keras.initializers import HeNormal
from keras import regularizers
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# ───────────────────────────────
# Load env and initialize supabase
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BUCKET_NAME = "uploads"

RETRAIN_FOLDER = "retraining_data"
os.makedirs(RETRAIN_FOLDER, exist_ok=True)

MODEL_PATH = "second_80_percent_model_ian_g_cnn_model.h5"


app = FastAPI()
request_counter = 0        
total_response_time = 0.0 

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    global request_counter, total_response_time

    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    request_counter += 1
    total_response_time += duration
    return response

@app.on_event("startup")
@repeat_every(seconds=60)
async def log_system_metrics() -> None:
    global request_counter, total_response_time

    if request_counter == 0:
        return

    avg_time = total_response_time / request_counter

    supabase.table("System_Metrics").insert({
        "timestamp": datetime.utcnow().isoformat(),
        "request_count": request_counter,
        "avg_response_time": avg_time,
        "model_uptime_status": "active"
    }).execute()

    request_counter = 0
    total_response_time = 0.0

@app.get("/testing_route")
def test_route():
    return {"message": "Testing and working"}


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        start_time = time.time()
        result = predict_image(file_path)
        response_time_ms = int((time.time() - start_time) * 1000)

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        supabase.storage.from_(BUCKET_NAME).upload(
            path=f"uploads/{unique_filename}",
            file=file_bytes,
            file_options={"content-type": file.content_type},
        )

        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(f"uploads/{unique_filename}")

        supabase.table("Predict").insert({
            "image_path": public_url,
            "predicted_class": result["predicted_class"],
            "confidence_score": result["confidence"],
            "response_time": response_time_ms,
        }).execute()

        os.remove(file_path)

        return JSONResponse(content={**result, "file_url": public_url})

    except Exception as e:
        print("Error in /predict endpoint:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/upload-zip/")
async def upload_zip(zip_file: UploadFile = File(...)):
    if not zip_file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are accepted")

    temp_zip_path = f"temp_{uuid.uuid4().hex}.zip"
    async with aiofiles.open(temp_zip_path, "wb") as out_file:
        content = await zip_file.read()
        await out_file.write(content)

    if os.path.exists(RETRAIN_FOLDER):
        shutil.rmtree(RETRAIN_FOLDER)
    os.makedirs(RETRAIN_FOLDER, exist_ok=True)

    try:
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(RETRAIN_FOLDER)
    except zipfile.BadZipFile:
        os.remove(temp_zip_path)
        raise HTTPException(status_code=400, detail="Corrupted zip file")

    os.remove(temp_zip_path)

    new_rows = []
    for label_folder in os.listdir(RETRAIN_FOLDER):
        label_path = os.path.join(RETRAIN_FOLDER, label_folder)
        if not os.path.isdir(label_path):
            continue

        for file_name in os.listdir(label_path):
            full_path = os.path.join(label_path, file_name)
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue

            new_rows.append({
                "image_path": full_path,
                "shoe_class": label_folder,
                "is_processed": False,
                "uploaded_at": datetime.utcnow().isoformat()
            })

    for row in new_rows:
        supabase.table("Training_Data").insert(row).execute()

    return {
        "message": f"{len(new_rows)} images extracted and saved.",
        "labels": list(set([r['shoe_class'] for r in new_rows]))
    }


def build_model():
    model = Sequential(name='Ian_G_CNN')

    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu',
                     kernel_regularizer=regularizers.l2(0.001),
                     kernel_initializer=HeNormal(), input_shape=(128, 128, 3), name='CONV_Layer1'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(BatchNormalization())

    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu',
                     kernel_initializer=HeNormal(), name='CONV_Layer2'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(BatchNormalization())
    model.add(Dropout(0.40))

    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu',
                     kernel_initializer=HeNormal(), name='CONV_Layer3'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(BatchNormalization())
    model.add(Dropout(0.40))

    model.add(Flatten(name='Flatten'))

    model.add(Dense(220, activation='relu', kernel_initializer=HeNormal(), name='FullyConnected1'))
    model.add(Dense(64, activation="relu"))

    model.add(Dense(3, activation='softmax', kernel_initializer=HeNormal(), name='OutputLayer'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def load_images_and_labels(records):
    images = []
    labels = []

    for item in records:
        path = item['image_path']
        label = item['shoe_class']
        try:
            img = Image.open(path).convert('RGB').resize((128, 128))
            img = np.array(img) / 255.0
            images.append(img)
            labels.append(label)
        except Exception as e:
            print(f"Error loading {path}: {e}")

    return np.array(images), np.array(labels)


@app.post("/retrain/")
def retrain_model():
    try:
        response = supabase.table("Training_Data").select("*").eq("is_processed", False).execute()
        records = response.data

        if not records:
            return JSONResponse(status_code=404, content={"message": "No new training data found."})

        X, y = load_images_and_labels(records)
        if len(X) == 0:
            return JSONResponse(status_code=400, content={"message": "No valid images found for retraining."})

        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        y_cat = to_categorical(y_encoded)

        # Load or build model
        if os.path.exists(MODEL_PATH):
            model = load_model(MODEL_PATH)
            print("Loaded existing model for retraining.")
        else:
            model = build_model()
            print("Built new model for training.")

        # Retrain model
        model.fit(X, y_cat, epochs=3, batch_size=16)

        # Save updated model
        model.save(MODEL_PATH)

        # Mark Training_Data as processed
        ids_to_update = [item['id'] for item in records]
        for record_id in ids_to_update:
            supabase.table("Training_Data").update({"is_processed": True}).eq("id", record_id).execute()

        return {"message": f"Retrained on {len(X)} samples", "labels": list(np.unique(y))}
    
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
