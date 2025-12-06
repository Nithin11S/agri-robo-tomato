import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import json
import os

# Page configuration
st.set_page_config(page_title="Leaf Disease Detection", page_icon="🍅", layout="centered")

# Title
st.title("🍅 Leaf Disease Detection")
st.markdown("---")

# Load model and class mapping
@st.cache_resource
def load_disease_model():
    """Load the trained model"""
    if os.path.exists('tomato_disease_model.h5'):
        model = load_model('tomato_disease_model.h5')
        return model
    else:
        return None

@st.cache_data
def load_class_mapping():
    """Load the class mapping"""
    if os.path.exists('class_mapping.json'):
        with open('class_mapping.json', 'r') as f:
            mapping = json.load(f)
        # Convert string keys to integers
        return {int(k): v for k, v in mapping.items()}
    else:
        return None

# Load model and mapping
model = load_disease_model()
class_mapping = load_class_mapping()

# Check if model and mapping are available
if model is None or class_mapping is None:
    st.error("⚠️ Model files not found! Please train the model first using cnn_train.py")
    st.info("Required files: tomato_disease_model.h5 and class_mapping.json")
    st.stop()

# Function to preprocess and predict
def predict_disease(image):
    """Preprocess image and make prediction"""
    try:
        # Display the image
        st.image(image, caption="Captured Image", use_container_width=True)
        
        # Preprocess image
        # Resize to 128x128 (same as training)
        image = image.resize((128, 128))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to array and normalize
        img_array = np.array(image)
        img_array = img_array.astype('float32') / 255.0  # Normalize to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        # Make prediction
        with st.spinner("Analyzing image..."):
            predictions = model.predict(img_array, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class_idx] * 100
        
        # Get disease name from mapping
        disease_name = class_mapping.get(predicted_class_idx, "Unknown")
        
        # Format disease name (remove "Tomato___" prefix and replace underscores)
        formatted_disease = disease_name.replace("Tomato___", "").replace("_", " ").title()
        
        # Display result
        st.markdown("---")
        st.subheader("🔍 Prediction Result")
        
        # Determine if it's healthy or diseased
        is_healthy = "healthy" in disease_name.lower()
        
        # Check confidence threshold
        if confidence < 50:
            st.error(f"⚠️ **Low Confidence Prediction** ({confidence:.2f}%)")
            st.warning("The model is uncertain about this prediction. Please verify the result or try a clearer image.")
        elif confidence < 70:
            st.warning(f"⚠️ **Moderate Confidence** ({confidence:.2f}%)")
            st.info("Consider verifying this result with additional images.")
        
        if is_healthy:
            st.success(f"✅ **Status:** {formatted_disease}")
        else:
            st.warning(f"⚠️ **Disease Detected:** {formatted_disease}")
        
        if confidence >= 50:
            st.info(f"**Confidence:** {confidence:.2f}%")
        
        # DEBUG: Show all predictions to help diagnose issues
        st.markdown("---")
        with st.expander("🔬 Debug: All Class Probabilities", expanded=False):
            prediction_dict = {}
            for idx, prob in enumerate(predictions[0]):
                class_name = class_mapping.get(idx, "Unknown")
                formatted_name = class_name.replace("Tomato___", "").replace("_", " ").title()
                prediction_dict[formatted_name] = prob * 100
            
            # Sort by probability
            sorted_predictions = sorted(prediction_dict.items(), key=lambda x: x[1], reverse=True)
            
            # Display all predictions in a table
            st.write("**Top 3 Predictions:**")
            for i, (name, prob) in enumerate(sorted_predictions[:3]):
                if i == 0:
                    st.write(f"🥇 **{name}**: {prob:.2f}%")
                elif i == 1:
                    st.write(f"🥈 **{name}**: {prob:.2f}%")
                else:
                    st.write(f"🥉 **{name}**: {prob:.2f}%")
            
            # Show healthy class probability specifically
            healthy_prob = prediction_dict.get("Healthy", 0)
            if healthy_prob < 50:
                st.warning(f"⚠️ **Healthy probability is only {healthy_prob:.2f}%** - Model may need retraining")
        
        return formatted_disease, confidence
        
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        st.info("Please make sure you provided a valid image.")
        return None, None

# Create tabs for different input methods
tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Camera"])

# Tab 1: File Upload
with tab1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a tomato leaf image file",
        type=['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'],
        help="Upload an image of a tomato leaf to detect the disease",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        predict_disease(image)
    else:
        st.info("👆 Please upload an image file to get started")

# Tab 2: Camera
with tab2:
    st.subheader("Camera Capture")
    st.write("Use your device camera to capture a photo of the diseased leaf")
    
    # Camera input
    camera_image = st.camera_input(
        "Take a picture",
        help="Position the diseased leaf in the camera view and click to capture"
    )
    
    if camera_image is not None:
        # Convert camera image to PIL Image
        image = Image.open(camera_image)
        predict_disease(image)
    else:
        st.info("📷 Click the button above to activate your camera and capture an image")

