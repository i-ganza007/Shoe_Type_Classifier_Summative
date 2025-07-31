import os
import shutil
import time
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from supabase import create_client, Client
from prediction import predict_image

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Local folder for temp storage
UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Supabase storage bucket
BUCKET_NAME = "uploads"

@app.get('/testing_route')
def test_route():
    return {'message': 'Testing and working'}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Save locally
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Start response timer
        start_time = time.time()

        # Run prediction
        result = predict_image(file_path)

        # Time taken
        response_time = int((time.time() - start_time) * 1000)

        # Upload to Supabase storage
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(
                path=f"uploads/{file.filename}",
                file=f.read(),
                file_options={"content-type": file.content_type}
            )

        # Get public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(f"uploads/{file.filename}")

        # Log prediction to Supabase table
        supabase.table("Predict").insert({
            "image_path": public_url,
            "predicted_class": result["predicted_class"],
            "confidence_score": result["confidence"],
            "response_time": response_time
        }).execute()

        # Delete local file
        os.remove(file_path)

        # Return result + image URL
        return JSONResponse(content={**result, "file_url": public_url})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
