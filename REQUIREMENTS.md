# Requirements Documentation

This document provides a comprehensive guide to all dependencies and requirements for the Agri ROBO Tomato project.

## Project Structure

```
tomato/
├── backend/              # Python FastAPI backend
│   ├── requirements.txt           # Backend API server dependencies
│   └── requirements-training.txt   # Additional dependencies for training
├── frontend/             # React + Vite frontend
│   ├── package.json      # Frontend dependencies (npm)
│   └── requirements.txt   # Documentation file
└── requirements.txt       # Root-level convenience file
```

## Backend Requirements

### For API Server Only

**File:** `backend/requirements.txt`

Install with:
```bash
cd backend
pip install -r requirements.txt
```

**Dependencies:**
- **FastAPI** (>=0.104.1) - Modern web framework
- **Uvicorn** (>=0.24.0) - ASGI server
- **TensorFlow** (>=2.10.0, <3.0.0) - ML framework for model inference
- **NumPy** (>=1.21.0, <2.0.0) - Numerical computing
- **Pillow** (>=9.0.0) - Image processing
- **Requests** (>=2.31.0) - HTTP library for testing

### For Model Training

**File:** `backend/requirements-training.txt`

Install with:
```bash
cd backend
pip install -r requirements-training.txt
```

**Additional Dependencies:**
- All dependencies from `requirements.txt`
- **pydot** (>=1.4.2) - Model visualization
- **graphviz** (>=0.20.0) - Graph visualization (requires system installation)
- **tqdm** (>=4.65.0) - Progress bars

**System Requirements for Training:**
- Python 3.8+
- 8GB+ RAM recommended
- GPU support optional but recommended
- 5GB+ free disk space for model files

## Frontend Requirements

**File:** `frontend/package.json`

Install with:
```bash
cd frontend
npm install
```

**Runtime Dependencies:**
- **React** (^18.2.0) - UI framework
- **React DOM** (^18.2.0) - React renderer
- **Axios** (^1.6.0) - HTTP client for API calls

**Development Dependencies:**
- **Vite** (^5.0.0) - Build tool and dev server
- **Tailwind CSS** (^3.3.5) - CSS framework
- **PostCSS** (^8.4.31) - CSS processor
- **Autoprefixer** (^10.4.16) - CSS vendor prefixer

**System Requirements:**
- Node.js 16+ (18.x or 20.x recommended)
- npm 8+ or yarn

## Quick Start

### Backend Setup

```bash
# Create virtual environment
python -m venv backend/venv

# Activate virtual environment
# Windows:
backend\venv\Scripts\Activate.ps1
# Linux/Mac:
source backend/venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Platform-Specific Notes

### Windows
- Use PowerShell for virtual environment activation
- Graphviz requires manual installation from [graphviz.org](https://graphviz.org/download/)

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-venv python3-pip nodejs npm graphviz

# For TensorFlow GPU support (optional)
sudo apt-get install nvidia-cuda-toolkit
```

### macOS
```bash
# Install system dependencies
brew install python3 node graphviz

# For TensorFlow GPU support (optional)
brew install caskroom/cask/cuda
```

### Raspberry Pi
- Use `tensorflow-lite` instead of full TensorFlow for better performance
- Install ARM-compatible versions of dependencies
- Consider training on a more powerful machine and deploying the model

## Version Compatibility

| Component | Minimum Version | Recommended Version |
|-----------|----------------|---------------------|
| Python | 3.8 | 3.10+ |
| Node.js | 16.x | 18.x or 20.x |
| TensorFlow | 2.10.0 | 2.15+ |
| FastAPI | 0.104.1 | Latest |
| React | 18.2.0 | Latest 18.x |

## Troubleshooting

### TensorFlow Installation Issues
- **Windows:** Ensure Visual C++ Redistributable is installed
- **Linux:** May need to install `python3-dev` and `build-essential`
- **macOS:** May need Xcode Command Line Tools

### Graphviz Issues
- Graphviz requires system-level installation before Python package
- Verify installation: `dot -V`

### Node.js Version Issues
- Use `nvm` (Node Version Manager) to switch versions
- Ensure npm version matches Node.js version

## Production Deployment

### Backend
- Pin exact versions in `requirements.txt` for reproducibility
- Use `pip freeze > requirements-lock.txt` to capture exact versions
- Consider using Docker for consistent environments

### Frontend
- Build production bundle: `npm run build`
- Serve static files from `dist/` folder
- Configure reverse proxy (nginx) for production

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow Installation Guide](https://www.tensorflow.org/install)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

