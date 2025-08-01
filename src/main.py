import os
import shutil
import time
from datetime import datetime
import traceback
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every      # <─ NEW
from dotenv import load_dotenv
from supabase import create_client, Client

from prediction import predict_image

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")          
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

BUCKET_NAME = "uploads"

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

    # nothing to write yet
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

import uuid
import traceback
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

        # Get public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(f"uploads/{unique_filename}")

        supabase.table("Predict").insert({
            "image_path": public_url,
            "predicted_class": result["predicted_class"],
            "confidence_score": result["confidence"],
            "response_time": response_time_ms,
        }).execute()

        # Clean up local file
        os.remove(file_path)

        # Return prediction + URL
        return JSONResponse(content={**result, "file_url": public_url})

    except Exception as e:
        import traceback
        print("Error in /predict endpoint:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

