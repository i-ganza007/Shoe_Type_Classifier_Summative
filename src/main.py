import os
import shutil
from fastapi.responses import JSONResponse
from fastapi import FastAPI , UploadFile , File
from pydantic import BaseModel
import uvicorn
from prediction import predict_image


app = FastAPI()

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get('/testing_route')
def test_route():
    return 'Testing and working'

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predict_image(file_path)
        os.remove(file_path)

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)