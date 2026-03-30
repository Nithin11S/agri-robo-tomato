# Agri ROBO - Tomato Disease Detection System

A web application for detecting tomato leaf diseases using AI, with robot control capabilities for Raspberry Pi deployment.

## Features

- Disease detection from uploaded or captured leaf images
- Robot motor control
- Fertilizer dispenser servo control
- Desktop camera support, with Raspberry Pi camera support where available

## Prerequisites

- Python 3.8+ (3.10+ recommended)
- Node.js 16+ and npm
- Trained model files in the project root:
  - `tomato_disease_model.h5` or `tomato_disease_model_best.h5`
  - `class_mapping.json`

## Installation

Place the trained model files in the project root before starting the backend.

### Windows

#### Install Backend Dependencies

```powershell
cd "C:\path\to\tomato"
python -m venv backend\venv
.\backend\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once and then try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

If you hit a NumPy install issue on Python 3.13:

```powershell
pip install --only-binary :all: numpy
pip install -r requirements.txt
```

#### Install Frontend Dependencies

```powershell
cd "C:\path\to\tomato\frontend"
npm install
```

### macOS

#### Install Backend Dependencies

```bash
cd /path/to/tomato
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r requirements.txt
```

If `pip` points to the wrong Python, use:

```bash
python3 -m pip install -r requirements.txt
```

#### Install Frontend Dependencies

```bash
cd /path/to/tomato/frontend
npm install
```

## Running the Application

### Windows

#### Start Backend Server

```powershell
cd "C:\path\to\tomato"
.\backend\venv\Scripts\Activate.ps1
cd backend
python main.py
```

#### Start Frontend Server

Open a new terminal:

```powershell
cd "C:\path\to\tomato\frontend"
npm run dev
```

### macOS

#### Start Backend Server

```bash
cd /path/to/tomato
source backend/venv/bin/activate
cd backend
python main.py
```

#### Start Frontend Server

Open a new terminal:

```bash
cd /path/to/tomato/frontend
npm run dev
```

Backend runs on: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`  
Frontend runs on: `http://localhost:3000`

For normal local development, only `npm run dev` is needed. No frontend build output folder is required unless you later choose to make a production build.

## Project Structure

```text
tomato/
|-- backend/              # FastAPI backend
|   `-- main.py           # API server
|-- frontend/             # React frontend
|   |-- src/              # Source code
|   `-- package.json      # Node dependencies
|-- requirements.txt      # Python dependencies
|-- class_mapping.json    # Class index mapping
`-- *.h5                  # Pre-trained model files (not in git)
```

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `POST /api/detect-disease` - Detect disease from image
- `POST /api/motor/control?direction={direction}` - Control motors
- `POST /api/servo/control?action={action}` - Control servo

## Requirements

See `requirements.txt` for Python dependencies.  
See `frontend/package.json` for Node.js dependencies.

## Technologies

- Backend: FastAPI, TensorFlow, Keras, PIL
- Frontend: React, Vite, Tailwind CSS, Axios
- ML: TensorFlow/Keras for disease classification

## License

MIT License
