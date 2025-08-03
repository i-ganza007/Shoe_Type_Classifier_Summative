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
├── src/
│   ├── model.py               # FastAPI app entrypoint
│   ├── prediction.py          # Prediction logic
│   ├── preprocessing.py       # Image preprocessing functions
│   ├── locustfile.py          # Load testing configuration
│   └── second_80_percent_model_ian_g_cnn_model.h5  # Trained model
├── performance_testing/
│   ├── Locust_2025-08-03-10h39_requests.csv       # Raw test data
│   ├── total_requests_per_second.png              # RPS visualization
│   ├── response_times.png                         # Response time charts
│   └── number_of_users.png                        # User load progression
├── models/
│   └── ian_g_cnn_model.h5     # Model versions
├── dataset/
│   └── split_data/            # Training/validation/test data
├── temp_uploads/              # Temporary folder for uploaded images
├── requirements.txt           # Dependencies
├── runtime.txt               # Python version for deployment
├── .python-version          # Python version specification
├── Procfile                 # Heroku deployment config
├── vercel.json             # Vercel deployment config
├── DEPLOYMENT.md           # Deployment instructions
└── README.md               # This file
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

## 📊 **Performance Testing Results (Locust)**

**Load Test Date**: August 3, 2025  
**Target**: [https://shoe-type-classifier-summative.onrender.com/predict](https://shoe-type-classifier-summative.onrender.com/predict)  
**Test Tool**: Locust Load Testing Framework

### 📋 **Test Data & Visualizations**

📊 **Raw Data**: [Locust CSV Results](./performance_testing/Locust_2025-08-03-10h39_locustfile.py_https___shoe-type-classifier-summative.onrender.com_requests.csv)  
📈 **Performance Charts**: 
- [Total Requests per Second](./performance_testing/total_requests_per_second.png)
- [Response Times Distribution](./performance_testing/response_times.png)  
- [Number of Users Over Time](./performance_testing/number_of_users.png)

### 📈 **Test Results Summary**

| Metric | Value |
|--------|-------|
| **Total Requests** | 37 |
| **Failure Rate** | 0% (100% Success Rate!) |
| **Average Response Time** | 8,685 ms (~8.7 seconds) |
| **Median Response Time** | 2,400 ms (2.4 seconds) |
| **Min Response Time** | 1,315 ms |
| **Max Response Time** | 51,181 ms |
| **Requests per Second** | 0.485 |
| **Concurrent Users** | 5 users |

### 🎯 **Performance Insights**

✅ **100% Success Rate** - No failed requests!  
✅ **Stable Under Load** - Handled concurrent users effectively  
⚡ **Fast Median Response** - 50% of requests completed in under 2.4 seconds  
🔄 **ML Processing Time** - Higher average due to TensorFlow model inference  

### 📊 **Response Time Distribution**

- **50th percentile**: 2,400 ms
- **75th percentile**: 2,900 ms  
- **90th percentile**: 50,000 ms
- **95th percentile**: 51,000 ms

*Note: Higher percentiles show some requests took longer due to cold starts and ML model processing time, which is normal for ML APIs on cloud platforms.*

### 📊 **Visual Performance Analysis**

The Locust testing generated comprehensive performance charts showing:

1. **📈 Total Requests per Second**: Demonstrates the API's throughput capability, reaching peak performance of ~1.5 RPS
2. **⏱️ Response Times Distribution**: Shows 50th vs 95th percentile response times, with most requests completing quickly
3. **👥 User Load Progression**: Visualizes how the system handled gradual user ramp-up from 0 to 5 concurrent users

### 🔬 **Test Configuration**

- **Test Duration**: ~3 minutes
- **User Simulation**: Gradual ramp-up to 5 concurrent users
- **Request Pattern**: Continuous POST requests to `/predict` endpoint
- **Image Upload**: Real shoe image (D111.jpeg) for authentic ML processing load
- **Wait Time**: 1-2 seconds between requests per user (realistic usage pattern)

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
