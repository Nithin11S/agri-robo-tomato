"""Quick test to verify model loads correctly"""
import os
import json
from tensorflow.keras.models import load_model

print("Testing model loading...")
print("="*70)

# Get paths
project_root = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_root, 'tomato_disease_model_best.h5')
mapping_path = os.path.join(project_root, 'class_mapping.json')

# Check files exist
if not os.path.exists(model_path):
    print(f"[ERROR] Model not found: {model_path}")
    exit(1)
if not os.path.exists(mapping_path):
    print(f"[ERROR] Mapping not found: {mapping_path}")
    exit(1)

print(f"[OK] Model file found: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
print(f"[OK] Mapping file found")

# Load model
try:
    print("\nLoading model...")
    model = load_model(model_path, compile=False)
    print(f"[OK] Model loaded! Input shape: {model.input_shape}")
    print(f"[OK] Number of outputs: {model.output_shape[1]}")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    exit(1)

# Load mapping
try:
    with open(mapping_path) as f:
        mapping = json.load(f)
    print(f"[OK] Class mapping loaded: {len(mapping)} classes")
    print("\nClasses:")
    for idx, name in sorted(mapping.items(), key=lambda x: int(x[0])):
        print(f"  {idx}: {name}")
except Exception as e:
    print(f"[ERROR] Error loading mapping: {e}")
    exit(1)

print("\n" + "="*70)
print("[OK] All checks passed! Model is ready to use.")
print("="*70)
