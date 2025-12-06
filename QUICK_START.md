# Quick Start Guide

## Verify Model Connection

The CNN model from `cnn_train.py` is now fully connected to the FastAPI backend.

### What Was Done:

1. **Backend (`backend/main.py`)**:
   - ✅ Loads model from `tomato_disease_model.h5` or `tomato_disease_model_best.h5`
   - ✅ Loads class mapping from `class_mapping.json`
   - ✅ Preprocesses images to match training (128x128, RGB, normalized)
   - ✅ Makes predictions using the trained CNN model
   - ✅ Returns formatted results with confidence scores

2. **Frontend (`frontend/src/components/DiseaseDetection.jsx`)**:
   - ✅ Image upload functionality
   - ✅ Camera capture functionality
   - ✅ API integration for disease detection
   - ✅ Results display with confidence scores

## Testing the Connection

### 1. Check if Model Files Exist:
```bash
# Should see these files in the project root:
ls tomato_disease_model*.h5
ls class_mapping.json
```

### 2. Test Model Loading:
```bash
cd backend
python test_model.py
```

Expected output:
```
✓ Model loaded successfully!
✓ Class mapping loaded!
✓ Prediction successful!
```

### 3. Start Backend:
```bash
cd backend
python main.py
```

You should see:
```
Model and class mapping loaded successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Start Frontend:
```bash
cd frontend
npm install  # First time only
npm run dev
```

### 5. Test in Browser:
1. Open `http://localhost:3000`
2. Go to "Leaf Disease Detection" section
3. Upload an image or use camera
4. Click "Detect Disease"
5. See results!

### 6. Test via API (Alternative):
```bash
python test_upload.py train/Tomato___healthy/0.JPG
```

## Troubleshooting

### Model Not Found Error:
- Run `python cnn_train.py` to generate model files
- Make sure `tomato_disease_model.h5` and `class_mapping.json` are in the project root

### API Connection Error:
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify frontend proxy in `frontend/vite.config.js`

### Image Processing Error:
- Ensure image is a valid format (JPG, PNG, etc.)
- Check image size (will be resized to 128x128 automatically)
- Verify image is not corrupted

## Model Details

- **Input Size**: 128x128 pixels, RGB
- **Preprocessing**: Resize to 128x128, convert to RGB, normalize to [0,1]
- **Output**: 10 disease classes
- **Architecture**: CNN with Conv2D, MaxPooling2D, Dense layers
- **Training**: See `cnn_train.py` for details

