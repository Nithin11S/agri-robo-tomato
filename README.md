# 🍅 Agri ROBO - Tomato Disease Detection System

A modern web application for detecting tomato leaf diseases using AI, with robot control capabilities for Raspberry Pi deployment.

## Features

- 🔍 **Disease Detection**: Upload or capture images to detect tomato leaf diseases using TensorFlow/Keras
- 🤖 **Robot Motor Control**: Control robot movement (Front, Back, Left, Right, Stop)
- 💧 **Fertilizer Dispenser**: Control servo motor for fertilizer dispensing (Start/Stop)
- 📷 **Camera Integration**: Desktop camera support (ready for Pi Camera)

## Project Structure

```
tomato/
├── backend/              # FastAPI backend
│   ├── main.py          # API server
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── ...
│   └── package.json     # Node dependencies
├── app.py               # Original Streamlit app (reference)
└── tomato_disease_model.h5  # Trained model
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- TensorFlow model files (`tomato_disease_model.h5` and `class_mapping.json`)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure the model files are in the parent directory:
   - `tomato_disease_model.h5`
   - `class_mapping.json`

5. Start the FastAPI server:
```bash
python main.py
# Or using uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

### Step 1: Ensure Model Files Exist

Before starting, make sure you have the trained model files:
- `tomato_disease_model.h5` or `tomato_disease_model_best.h5`
- `class_mapping.json`

If these files don't exist, train the model first:
```bash
python cnn_train.py
```

### Step 2: Test Model Connection (Optional)

Test if the model loads correctly:
```bash
cd backend
python test_model.py
```

This will verify:
- Model file exists and can be loaded
- Class mapping file exists and is valid
- Model can make predictions

### Step 3: Start the Application

1. **Start Backend**: Run the FastAPI server (port 8000)
```bash
cd backend
python main.py
# Or: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start Frontend** (in a new terminal): Run the React dev server (port 3000)
```bash
cd frontend
npm install  # First time only
npm run dev
```

3. **Open Browser**: Navigate to `http://localhost:3000`

### Step 4: Test Disease Detection

#### Via Web Interface:
- Click "Upload Image" to select a file, or
- Click "Open Camera" to capture an image
- Click "Detect Disease" to analyze the image
- View results with confidence scores and top predictions

#### Via API (Command Line):
```bash
python test_upload.py train/Tomato___healthy/0.JPG
```

#### Check API Health:
```bash
curl http://localhost:8000/health
```

### Motor Control

- Use the directional buttons to control robot movement
- Currently sends API requests (GPIO implementation pending)

### Servo Control

- Use Start/Stop buttons to control fertilizer dispensing
- Currently sends API requests (GPIO implementation pending)

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check (shows model loading status)
- `POST /api/detect-disease` - Detect disease from image
  - Body: `multipart/form-data` with `file` field containing image
  - Returns: JSON with disease name, confidence, and top predictions
- `POST /api/motor/control?direction={direction}` - Control motors
- `POST /api/servo/control?action={action}` - Control servo

### Testing API with curl:
```bash
curl -X POST "http://localhost:8000/api/detect-disease" \
  -F "file=@path/to/image.jpg"
```

## Future Implementation

When Raspberry Pi is available:

1. **GPIO Integration**: 
   - Install `RPi.GPIO` or `gpiozero` library
   - Implement motor control using GPIO pins
   - Implement servo control using PWM

2. **Pi Camera**:
   - Replace desktop camera with Pi Camera module
   - Use `picamera2` library for camera access

3. **Production Deployment**:
   - Build React app: `npm run build`
   - Serve static files with FastAPI or nginx
   - Set up systemd service for auto-start

## Technologies Used

- **Backend**: FastAPI, TensorFlow, Keras, PIL
- **Frontend**: React, Vite, Tailwind CSS, Axios
- **ML**: TensorFlow/Keras for disease classification

## License

MIT License

