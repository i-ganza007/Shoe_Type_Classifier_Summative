# 👟 Shoe Classifier with Online Retraining & Supabase Integration

A cloud-deployed machine learning system for classifying shoe images (Boot, Sandal, Shoe). Includes UI for uploading images, retraining with new data via zip files, real-time prediction, and Supabase integration for database + file storage.

## 🌐 **Live Demo & Links**

🎥 **YouTube Demo**: [Watch the Video Demo](https://youtu.be/ahVeuyan_wo)  
🚀 **Live API Backend**: [https://shoe-type-classifier-summative.onrender.com](https://shoe-type-classifier-summative.onrender.com)  
🎨 **StreamLit Frontend**: [https://classingshoe.streamlit.app/](https://classingshoe.streamlit.app/)  
📱 **Frontend Repository**: [StreamLit App GitHub](https://github.com/i-ganza007/StreamLit_App)

---

## 🔧 Features

✅ Image classification using a custom-trained deep learning model
✅ Upload shoe images for prediction
✅ Upload new data (as ZIP) for **retraining the model online**
✅ Automatically logs uploaded data in Supabase (`Training_Data` table)
✅ Saves predictions to Supabase (`Predict` table)
✅ UI/Web Interface for interaction
✅ Includes FastAPI backend with endpoints for:

* `/predict`: Predict shoe class
* `/retrain`: Retrain model with uploaded labeled images
* `/upload`: Store data for future retraining

---

## 📁 Project Structure

```
project-root/
│
├── main.py                # FastAPI app entrypoint
├── model/
│   └── model.h5           # Current trained model (overwritten after retraining)
├── training/
│   ├── retrain.py         # Logic for model retraining
│   └── preprocessing.py   # Image preprocessing functions
├── utils/
│   ├── supabase_client.py # Upload + DB utility functions
│   └── helper.py          # Utility helpers
├── temp_uploads/          # Temporary folder for uploaded images
├── uploads/               # Folder for zip upload files
├── README.md
└── requirements.txt
```

---

## 🦪 Usage Instructions

### 🔮 1. Prediction

* Upload an image via UI or `/predict` endpoint
* Prediction result and image path saved to `Predict` table in Supabase

### 📦 2. Retraining (via UI or `/retrain`)

#### Zip Format

```
your_zip_file.zip
└── Shoe/                  # Folder name = label
    ├── image1.jpg
    └── image2.jpg
└── Sandal/
    └── ...
└── Boot/
    └── ...
```

* Upload ZIP through `/retrain` endpoint
* Images are:

  * Extracted to `temp_uploads/`
  * Logged in `Training_Data` table
  * Preprocessed and used to retrain model
* **Old model is overwritten**

### 🗃️ 3. Supabase Tables

* `Predict`: stores predictions (`image_path`, `label`, `timestamp`)
* `Training_Data`: logs all retraining uploads (`image_path`, `shoe_class`, `is_processed`)

---

## 🎥 Final Submission Checklist

✅ **Video Demo**: [YouTube Demo Video](https://youtu.be/ahVeuyan_wo)

* [x] Camera on
* [x] Upload + Retrain workflow shown clearly
* [x] Prediction result demonstrated

✅ **Live Deployment**: [Render API](https://shoe-type-classifier-summative.onrender.com) + [StreamLit Frontend](https://classingshoe.streamlit.app/)

✅ Code includes:

* [x] Custom model retraining logic
* [x] Prediction logic
* [x] Supabase integration
* [x] Model evaluation metrics in training script (accuracy, F1, etc.)

✅ Deployment:

* [x] Web UI ([StreamLit Frontend](https://classingshoe.streamlit.app/))
* [x] Swagger/API testing interface ([API Docs](https://shoe-type-classifier-summative.onrender.com/docs))
* [x] Supabase DB + Storage used correctly

---

## 🚀 Installation & Run Locally

```bash
git clone https://github.com/i-ganza007/Shoe_Type_Classifier_Summative.git
cd Shoe_Type_Classifier_Summative
pip install -r requirements.txt
cd src
uvicorn model:app --reload
```

**Live API**: The app is already deployed at [https://shoe-type-classifier-summative.onrender.com](https://shoe-type-classifier-summative.onrender.com)

---

## 🥺 API Endpoints

| Endpoint   | Method | Description                                  | Live URL |
| ---------- | ------ | -------------------------------------------- | -------- |
| `/predict` | POST   | Upload an image for prediction               | [Test Live](https://shoe-type-classifier-summative.onrender.com/predict) |
| `/retrain` | POST   | Upload ZIP for model retraining              | [Test Live](https://shoe-type-classifier-summative.onrender.com/retrain) |
| `/upload`  | POST   | Upload data to Supabase only (no retraining) | [Test Live](https://shoe-type-classifier-summative.onrender.com/upload) |
| `/docs`    | GET    | Interactive API documentation                | [Swagger UI](https://shoe-type-classifier-summative.onrender.com/docs) |

**Frontend Interface**: Use the [StreamLit App](https://classingshoe.streamlit.app/) for a user-friendly interface!

---

## 🛠 Tech Stack

* Python + FastAPI
* TensorFlow/Keras (Image Classification)
* Supabase (PostgreSQL + Storage)
* Uvicorn
* HTML/CSS UI or Swagger/Postman

---

## 📧 Contact

Project by **IAN GANZA**

🎥 **Demo Video**: [YouTube](https://youtu.be/ahVeuyan_wo)  
🚀 **Live API**: [Render Deployment](https://shoe-type-classifier-summative.onrender.com)  
🎨 **Frontend**: [StreamLit App](https://classingshoe.streamlit.app/)  
📱 **Frontend Code**: [GitHub Repository](https://github.com/i-ganza007/StreamLit_App)  

For issues, please raise them in the [GitHub Issues](https://github.com/i-ganza007/Shoe_Type_Classifier_Summative/issues) section.
