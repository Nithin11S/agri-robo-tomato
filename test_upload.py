"""
Quick test script to test image upload and disease detection via API.
Usage: python test_upload.py <path_to_image>
"""

import sys
import requests
import os

def test_api_upload(image_path):
    """Test the disease detection API with an image"""
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return False
    
    api_url = "http://localhost:8000/api/detect-disease"
    
    print(f"Testing API with image: {image_path}")
    print(f"API URL: {api_url}")
    print("-" * 60)
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Success!")
            print(f"\nDisease: {result['disease']}")
            print(f"Confidence: {result['confidence']}%")
            print(f"Healthy: {result['is_healthy']}")
            print(f"\nTop 3 Predictions:")
            for i, pred in enumerate(result['top_predictions'], 1):
                print(f"  {i}. {pred['name']}: {pred['confidence']}%")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API.")
        print("  Make sure the backend server is running:")
        print("  cd backend && python main.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_upload.py <path_to_image>")
        print("Example: python test_upload.py train/Tomato___healthy/0.JPG")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_api_upload(image_path)
    sys.exit(0 if success else 1)

