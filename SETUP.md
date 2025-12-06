# Setup Guide for Team Members

This guide will help you set up the Agri ROBO Tomato project on your local machine.

## Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **Node.js 16+** (18.x or 20.x recommended)
- **npm** or **yarn**
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Nithin11S/agri-robo-tomato.git
cd agri-robo-tomato
```

### 2. Backend Setup

#### Create Virtual Environment

**Windows:**
```powershell
python -m venv backend/venv
backend\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
```

#### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Note:** If you encounter NumPy installation issues on Python 3.13, install it first:
```bash
pip install --only-binary :all: numpy
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Download or Train Model

The trained model files (`.h5`) are not included in the repository due to their large size. You have two options:

#### Option A: Train Your Own Model (Recommended for Development)

```bash
# Activate virtual environment first
backend\venv\Scripts\Activate.ps1  # Windows
# or
source backend/venv/bin/activate  # Linux/Mac

# Train the model (takes 1-3 hours)
python cnn_train_transfer_learning.py
```

#### Option B: Download Pre-trained Model

1. Download the model files from a shared location (Google Drive, Dropbox, etc.)
2. Place them in the project root:
   - `tomato_disease_model_best.h5` (or `tomato_disease_model.h5`)
   - `class_mapping.json`

### 5. Download Training Data (Optional)

If you want to retrain the model, you'll need the training data:

1. Download the dataset from the shared location
2. Extract to project root:
   - `train/` folder (contains training images)
   - `val/` folder (contains validation images)

**Note:** Training data is large (~1-2 GB) and not included in Git.

## Running the Application

### Start Backend Server

**Windows:**
```powershell
.\start_backend.ps1
# or
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

**Linux/Mac:**
```bash
cd backend
source venv/bin/activate
python main.py
```

The backend will run on `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173`

## Project Structure

```
agri-robo-tomato/
├── backend/              # FastAPI backend
│   ├── main.py           # Main API server
│   ├── requirements.txt  # Python dependencies
│   └── venv/             # Virtual environment (not in git)
├── frontend/             # React + Vite frontend
│   ├── src/              # Source code
│   ├── package.json      # Node dependencies
│   └── node_modules/     # Node modules (not in git)
├── train/                # Training data (not in git)
├── val/                  # Validation data (not in git)
├── *.h5                  # Model files (not in git)
├── cnn_train*.py         # Training scripts
├── requirements.txt      # Root requirements
└── README.md             # Project documentation
```

## Troubleshooting

### Backend Issues

**ModuleNotFoundError: No module named 'tensorflow'**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r backend/requirements.txt`

**Model file not found**
- Train the model or download it from shared location
- Ensure `tomato_disease_model_best.h5` and `class_mapping.json` are in project root

### Frontend Issues

**npm install fails**
- Clear cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then reinstall

**API connection errors**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

### Python Version Issues

**NumPy build errors (Python 3.13)**
```bash
pip install --only-binary :all: numpy
pip install -r backend/requirements.txt
```

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test locally
4. Commit: `git commit -m "Description of changes"`
5. Push: `git push origin feature/your-feature-name`
6. Create a Pull Request on GitHub

## Environment Variables

If you need to add environment variables:

1. Create a `.env` file in the project root (not committed to git)
2. Add your variables:
   ```
   API_KEY=your_key_here
   DATABASE_URL=your_url_here
   ```
3. Load in Python: `from dotenv import load_dotenv; load_dotenv()`

## Getting Help

- Check `README.md` for project overview
- Check `REQUIREMENTS.md` for detailed dependency information
- Check `QUICK_START.md` for quick reference
- Open an issue on GitHub for bugs or questions

## Notes

- **Model files** and **training data** are excluded from Git due to size
- Each team member should train their own model or download from shared location
- Virtual environments (`venv/`) are excluded - each person creates their own
- Node modules (`node_modules/`) are excluded - run `npm install` after cloning

