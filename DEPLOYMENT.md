# Deployment Instructions for Cloud Platforms

## Requirements Files

**`requirements.txt`** - Main requirements file that works for both local development and deployment
**`requirements-cloud.txt`** - CPU-only version specifically for cloud deployment (if needed)

## Deployment Options

### Option 1: Use Main Requirements (Recommended)

1. Use the main `requirements.txt` file - it has flexible TensorFlow versions
2. Set the start command to: `cd src && uvicorn model:app --host 0.0.0.0 --port $PORT`

### Option 2: Use Cloud-Specific Requirements (If TensorFlow issues persist)

1. Use `requirements-cloud.txt` which uses `tensorflow-cpu` for better cloud compatibility
2. Set the start command to: `cd src && uvicorn model:app --host 0.0.0.0 --port $PORT`

## Environment Variables to Set in Your Deployment Platform

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TF_CPP_MIN_LOG_LEVEL=2
PYTHONUNBUFFERED=1
```

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
