# Deployment Instructions - Render (Recommended)

## Requirements Files

**`requirements.txt`** - Main requirements file optimized for Render deployment

## For Render Deployment (Primary Option)

1. **Repository**: Connect your GitHub repository
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `cd src && uvicorn model:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: Add the variables listed below
5. **Python Version**: Python 3.11+ (auto-detected)

### Render Setup Steps:
1. Go to https://render.com/
2. Create new **Web Service**
3. Connect your GitHub repository: `Shoe_Type_Classifier_Summative`
4. Configure settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd src && uvicorn model:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (see below)
6. Deploy!

## Environment Variables to Set in Render Dashboard

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TF_CPP_MIN_LOG_LEVEL=2
PYTHONUNBUFFERED=1
```

## For Vercel Deployment (Python Functions)

1. **Root Directory**: `Shoe_Type_Classifier_Summative` (your main project folder)
2. **Build Command**: `pip install -r requirements.txt`
3. **Output Directory**: Leave empty (auto-detected)
4. **Install Command**: `pip install -r requirements.txt`
5. **Framework Preset**: Other
6. **Configuration**: Uses `vercel.json` file (already created)
7. **Environment Variables**: Add the variables listed above

### Vercel Setup Steps:
1. Go to https://vercel.com/
2. Import your GitHub repository
3. Set **Root Directory** to: `Shoe_Type_Classifier_Summative`
4. Set **Build Command** to: `pip install -r requirements.txt`
5. Add environment variables in Vercel dashboard
6. Deploy!

## For Render Deployment

1. **Repository**: Connect your GitHub repository
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `cd src && uvicorn model:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: Add the variables listed above

## For Heroku Deployment

1. **Procfile exists**: `web: cd src && uvicorn model:app --host 0.0.0.0 --port $PORT`
2. **Requirements**: Uses `requirements.txt` automatically
3. **Config Vars**: Add the environment variables listed above

## Key Changes Made:

1. **Single Requirements File**: Combined all requirements into one comprehensive file
2. **Flexible TensorFlow**: Uses version ranges for better compatibility
3. **Cloud Alternative**: Created `requirements-cloud.txt` with `tensorflow-cpu` if needed
4. **Better Organization**: Clear sections and comments in requirements
5. **Development Options**: Optional dev packages (commented out)

## Troubleshooting

### If you get TensorFlow version errors:
- Try using `requirements-cloud.txt` instead
- Ensure your deployment platform supports the TensorFlow version

### If you get import errors:
- Check that your model file is in the correct location (`src/` directory)
- Verify all environment variables are set correctly

### If the app fails to start:
- Check the logs for specific error messages
- Ensure the start command points to the correct directory

## File Structure for Deployment:

```
project/
├── requirements.txt          # Main requirements (use this)
├── requirements-cloud.txt    # Alternative for CPU-only platforms
├── Procfile                 # For Heroku/similar platforms
├── src/
│   ├── model.py            # Main FastAPI app
│   ├── prediction.py       # Prediction logic
│   ├── preprocessing.py    # Image preprocessing
│   └── second_80_percent_model_ian_g_cnn_model.h5  # Your model
└── DEPLOYMENT.md           # This file
```
