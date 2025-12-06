# -*- coding: utf-8 -*-
"""
Improved CNN Training Script for Tomato Disease Detection
This script uses a better architecture and training strategy for improved accuracy.
"""

import numpy as np
import json
import os
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

# Set random seeds for reproducibility
np.random.seed(1337)
tf.random.set_seed(1337)

print("=" * 60)
print("Improved Tomato Disease Detection Model Training")
print("=" * 60)

# Configuration
IMG_SIZE = 224  # Increased from 128 for better feature extraction
BATCH_SIZE = 32  # Reduced batch size for better gradient updates
EPOCHS = 50  # More epochs with early stopping
NUM_CLASSES = 10

print(f"\nConfiguration:")
print(f"  - Image Size: {IMG_SIZE}x{IMG_SIZE}")
print(f"  - Batch Size: {BATCH_SIZE}")
print(f"  - Max Epochs: {EPOCHS}")
print(f"  - Number of Classes: {NUM_CLASSES}")

# Build improved CNN architecture
print("\n" + "=" * 60)
print("Building Improved CNN Architecture...")
print("=" * 60)

model = Sequential([
    # First Conv Block
    Conv2D(64, (3, 3), input_shape=(IMG_SIZE, IMG_SIZE, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    
    # Second Conv Block
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    
    # Third Conv Block
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    
    # Fourth Conv Block
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    
    # Flatten and Dense layers
    Flatten(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

# Compile with better optimizer settings
initial_learning_rate = 0.001
optimizer = Adam(learning_rate=initial_learning_rate, beta_1=0.9, beta_2=0.999)

model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy', 'top_3_accuracy']
)

print("\nModel Architecture:")
model.summary()

# Enhanced data augmentation for training
print("\n" + "=" * 60)
print("Setting up Data Augmentation...")
print("=" * 60)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,  # Increased rotation
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,  # Increased zoom
    horizontal_flip=True,
    vertical_flip=True,  # Added vertical flip
    fill_mode='nearest',
    brightness_range=[0.8, 1.2],  # Added brightness variation
    channel_shift_range=0.2  # Added color variation
)

# Validation data (only rescaling, no augmentation)
val_datagen = ImageDataGenerator(rescale=1./255)

print("\nTraining Data Generator:")
print("  - Rotation: ±30 degrees")
print("  - Shift: ±20%")
print("  - Zoom: ±30%")
print("  - Flip: Horizontal & Vertical")
print("  - Brightness: 80-120%")
print("  - Color shift: ±20%")

# Load datasets
print("\n" + "=" * 60)
print("Loading Datasets...")
print("=" * 60)

training_set = train_datagen.flow_from_directory(
    'train',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

validation_set = val_datagen.flow_from_directory(
    'val',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Get class mapping
label_map = training_set.class_indices
print(f"\nClass Indices: {label_map}")

# Calculate steps
steps_per_epoch = len(training_set)
validation_steps = len(validation_set)

print(f"\nDataset Information:")
print(f"  - Training samples: {training_set.samples}")
print(f"  - Validation samples: {validation_set.samples}")
print(f"  - Steps per epoch: {steps_per_epoch}")
print(f"  - Validation steps: {validation_steps}")

# Callbacks for better training
print("\n" + "=" * 60)
print("Setting up Training Callbacks...")
print("=" * 60)

# Early stopping - stop if validation loss doesn't improve
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,  # Increased patience
    restore_best_weights=True,
    verbose=1,
    mode='min'
)

# Model checkpoint - save best model
model_checkpoint = ModelCheckpoint(
    'tomato_disease_model_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1,
    mode='max',
    save_weights_only=False
)

# Learning rate reduction - reduce LR when validation loss plateaus
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,  # Reduce LR by half
    patience=5,  # Wait 5 epochs
    min_lr=1e-7,
    verbose=1,
    mode='min'
)

callbacks = [early_stopping, model_checkpoint, reduce_lr]

print("Callbacks configured:")
print("  - Early Stopping: patience=10")
print("  - Model Checkpoint: saves best model")
print("  - Learning Rate Reduction: factor=0.5, patience=5")

# Train the model
print("\n" + "=" * 60)
print("Starting Training...")
print("=" * 60)

history = model.fit(
    training_set,
    steps_per_epoch=steps_per_epoch,
    epochs=EPOCHS,
    validation_data=validation_set,
    validation_steps=validation_steps,
    callbacks=callbacks,
    verbose=1
)

# Save the final model
print("\n" + "=" * 60)
print("Saving Final Model...")
print("=" * 60)

model.save('tomato_disease_model.h5')
print('[OK] Saved final model as tomato_disease_model.h5')

# Save class mapping
reverse_label_map = {v: k for k, v in label_map.items()}
with open('class_mapping.json', 'w') as f:
    json.dump(reverse_label_map, f, indent=4)

print('[OK] Saved class mapping as class_mapping.json')
print(f'\nClass mapping: {reverse_label_map}')

# Print training summary
print("\n" + "=" * 60)
print("Training Summary")
print("=" * 60)

if len(history.history['accuracy']) > 0:
    final_train_acc = history.history['accuracy'][-1] * 100
    final_val_acc = history.history['val_accuracy'][-1] * 100
    best_val_acc = max(history.history['val_accuracy']) * 100
    
    print(f"\nFinal Training Accuracy: {final_train_acc:.2f}%")
    print(f"Final Validation Accuracy: {final_val_acc:.2f}%")
    print(f"Best Validation Accuracy: {best_val_acc:.2f}%")
    
    if 'top_3_accuracy' in history.history:
        final_top3 = history.history['top_3_accuracy'][-1] * 100
        print(f"Final Top-3 Accuracy: {final_top3:.2f}%")

print("\n" + "=" * 60)
print("Training Complete!")
print("=" * 60)
print("\nModel files saved:")
print("  - tomato_disease_model.h5 (final model)")
print("  - tomato_disease_model_best.h5 (best validation model)")
print("  - class_mapping.json (class labels)")

