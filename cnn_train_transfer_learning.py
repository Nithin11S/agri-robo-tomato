# -*- coding: utf-8 -*-
"""
Transfer Learning Training Script for Tomato Disease Detection
Uses MobileNetV2 pre-trained on ImageNet for better accuracy.
"""

import numpy as np
import json
import os
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

# Set random seeds for reproducibility
np.random.seed(1337)
tf.random.set_seed(1337)

print("=" * 60)
print("Transfer Learning Model Training (MobileNetV2)")
print("=" * 60)

# Configuration
IMG_SIZE = 224  # MobileNetV2 standard input size
BATCH_SIZE = 32
EPOCHS = 50
NUM_CLASSES = 10

print(f"\nConfiguration:")
print(f"  - Base Model: MobileNetV2 (pre-trained on ImageNet)")
print(f"  - Image Size: {IMG_SIZE}x{IMG_SIZE}")
print(f"  - Batch Size: {BATCH_SIZE}")
print(f"  - Max Epochs: {EPOCHS}")
print(f"  - Number of Classes: {NUM_CLASSES}")

# Load pre-trained MobileNetV2 (without top layers)
print("\n" + "=" * 60)
print("Loading Pre-trained MobileNetV2...")
print("=" * 60)

base_model = MobileNetV2(
    weights='imagenet',  # Pre-trained weights
    include_top=False,   # Don't include classification head
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Freeze base model layers initially (we'll unfreeze some later)
base_model.trainable = False

print(f"[OK] Base model loaded")
print(f"  - Total layers: {len(base_model.layers)}")
print(f"  - Trainable layers: {sum([1 for layer in base_model.layers if layer.trainable])}")

# Add custom classification head
print("\n" + "=" * 60)
print("Building Classification Head...")
print("=" * 60)

# Add global average pooling
x = base_model.output
x = GlobalAveragePooling2D()(x)

# Add dense layers
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)

# Output layer
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

# Create the full model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile model
initial_learning_rate = 0.0001  # Lower LR for transfer learning
optimizer = Adam(learning_rate=initial_learning_rate, beta_1=0.9, beta_2=0.999)

model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy', 'top_3_accuracy']
)

print("\nModel Architecture:")
model.summary()

# Enhanced data augmentation
print("\n" + "=" * 60)
print("Setting up Data Augmentation...")
print("=" * 60)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest',
    brightness_range=[0.8, 1.2],
    channel_shift_range=0.2
)

val_datagen = ImageDataGenerator(rescale=1./255)

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

label_map = training_set.class_indices
print(f"\nClass Indices: {label_map}")

steps_per_epoch = len(training_set)
validation_steps = len(validation_set)

print(f"\nDataset Information:")
print(f"  - Training samples: {training_set.samples}")
print(f"  - Validation samples: {validation_set.samples}")
print(f"  - Steps per epoch: {steps_per_epoch}")
print(f"  - Validation steps: {validation_steps}")

# Callbacks
print("\n" + "=" * 60)
print("Setting up Training Callbacks...")
print("=" * 60)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1,
    mode='min'
)

model_checkpoint = ModelCheckpoint(
    'tomato_disease_model_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1,
    mode='max',
    save_weights_only=False
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-7,
    verbose=1,
    mode='min'
)

callbacks = [early_stopping, model_checkpoint, reduce_lr]

# Phase 1: Train only the top layers (frozen base)
print("\n" + "=" * 60)
print("Phase 1: Training Top Layers (Base Model Frozen)")
print("=" * 60)

history1 = model.fit(
    training_set,
    steps_per_epoch=steps_per_epoch,
    epochs=20,  # Train top layers first
    validation_data=validation_set,
    validation_steps=validation_steps,
    callbacks=[model_checkpoint, reduce_lr],
    verbose=1
)

# Phase 2: Unfreeze some layers and fine-tune
print("\n" + "=" * 60)
print("Phase 2: Fine-tuning (Unfreezing Top Layers)")
print("=" * 60)

# Unfreeze the top layers of the base model
base_model.trainable = True

# Freeze bottom layers, unfreeze top layers
fine_tune_at = len(base_model.layers) - 30  # Unfreeze last 30 layers

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

print(f"  - Unfrozen layers: {sum([1 for layer in base_model.layers if layer.trainable])}")
print(f"  - Frozen layers: {sum([1 for layer in base_model.layers if not layer.trainable])}")

# Recompile with lower learning rate for fine-tuning
model.compile(
    optimizer=Adam(learning_rate=0.00001),  # Even lower LR for fine-tuning
    loss='categorical_crossentropy',
    metrics=['accuracy', 'top_3_accuracy']
)

# Continue training
history2 = model.fit(
    training_set,
    steps_per_epoch=steps_per_epoch,
    epochs=EPOCHS - 20,  # Remaining epochs
    validation_data=validation_set,
    validation_steps=validation_steps,
    callbacks=callbacks,
    verbose=1,
    initial_epoch=20
)

# Combine histories
history = {
    'accuracy': history1.history['accuracy'] + history2.history['accuracy'],
    'val_accuracy': history1.history['val_accuracy'] + history2.history['val_accuracy'],
    'loss': history1.history['loss'] + history2.history['loss'],
    'val_loss': history1.history['val_loss'] + history2.history['val_loss'],
}

if 'top_3_accuracy' in history1.history:
    history['top_3_accuracy'] = history1.history['top_3_accuracy'] + history2.history['top_3_accuracy']

# Save final model
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

# Print summary
print("\n" + "=" * 60)
print("Training Summary")
print("=" * 60)

if len(history['accuracy']) > 0:
    final_train_acc = history['accuracy'][-1] * 100
    final_val_acc = history['val_accuracy'][-1] * 100
    best_val_acc = max(history['val_accuracy']) * 100
    
    print(f"\nFinal Training Accuracy: {final_train_acc:.2f}%")
    print(f"Final Validation Accuracy: {final_val_acc:.2f}%")
    print(f"Best Validation Accuracy: {best_val_acc:.2f}%")
    
    if 'top_3_accuracy' in history:
        final_top3 = history['top_3_accuracy'][-1] * 100
        print(f"Final Top-3 Accuracy: {final_top3:.2f}%")

print("\n" + "=" * 60)
print("Training Complete!")
print("=" * 60)
print("\nModel files saved:")
print("  - tomato_disease_model.h5 (final model)")
print("  - tomato_disease_model_best.h5 (best validation model)")
print("  - class_mapping.json (class labels)")

