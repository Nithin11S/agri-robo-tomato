"""
Test script to verify the CNN model is properly loaded and can make predictions.
Run this to test the model connection before using the API.
"""

import os
import sys
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import json

def test_model_loading():
    """Test if model and mapping can be loaded"""
    print("=" * 60)
    print("Testing Model Connection")
    print("=" * 60)
    
    # Get paths
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(backend_dir)
    
    model_path_best = os.path.join(project_root, 'tomato_disease_model_best.h5')
    model_path = os.path.join(project_root, 'tomato_disease_model.h5')
    mapping_path = os.path.join(project_root, 'class_mapping.json')
    
    # Check files
    print("\n1. Checking model files...")
    if os.path.exists(model_path_best):
        model_path = model_path_best
        print(f"   ✓ Found best model: {model_path}")
    elif os.path.exists(model_path):
        print(f"   ✓ Found model: {model_path}")
    else:
        print(f"   ✗ Model not found!")
        print(f"     Checked: {model_path}")
        print(f"     Checked: {model_path_best}")
        print(f"     Please run cnn_train.py to generate the model.")
        return False
    
    if os.path.exists(mapping_path):
        print(f"   ✓ Found class mapping: {mapping_path}")
    else:
        print(f"   ✗ Class mapping not found!")
        print(f"     Checked: {mapping_path}")
        print(f"     Please run cnn_train.py to generate the class mapping.")
        return False
    
    # Load model
    print("\n2. Loading model...")
    try:
        model = load_model(model_path)
        print(f"   ✓ Model loaded successfully!")
        print(f"   - Input shape: {model.input_shape}")
        print(f"   - Output shape: {model.output_shape}")
    except Exception as e:
        print(f"   ✗ Error loading model: {e}")
        return False
    
    # Load mapping
    print("\n3. Loading class mapping...")
    try:
        with open(mapping_path, 'r') as f:
            mapping = json.load(f)
        class_mapping = {int(k): v for k, v in mapping.items()}
        print(f"   ✓ Class mapping loaded!")
        print(f"   - Number of classes: {len(class_mapping)}")
        print(f"   - Classes: {list(class_mapping.values())}")
    except Exception as e:
        print(f"   ✗ Error loading mapping: {e}")
        return False
    
    # Test prediction with dummy image
    print("\n4. Testing prediction with dummy image...")
    try:
        # Create a dummy RGB image (128x128)
        dummy_img = np.random.rand(128, 128, 3).astype(np.float32)
        dummy_img = np.expand_dims(dummy_img, axis=0)
        
        predictions = model.predict(dummy_img, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_idx] * 100
        
        disease_name = class_mapping.get(predicted_idx, "Unknown")
        formatted_disease = disease_name.replace("Tomato___", "").replace("_", " ").title()
        
        print(f"   ✓ Prediction successful!")
        print(f"   - Predicted: {formatted_disease}")
        print(f"   - Confidence: {confidence:.2f}%")
        print(f"   - All predictions sum: {np.sum(predictions[0]):.4f} (should be ~1.0)")
    except Exception as e:
        print(f"   ✗ Error making prediction: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ All tests passed! Model is ready to use.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_model_loading()
    sys.exit(0 if success else 1)

