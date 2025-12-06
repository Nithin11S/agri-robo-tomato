# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 17:17:40 2017

@author: Mohit
"""

#Part 1 : Building a CNN

#import Keras packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
import numpy as np
# from keras.utils.vis_utils import plot_model  # Commented out - not available in newer Keras versions


# Initializing the CNN

np.random.seed(1337)
classifier = Sequential()

classifier.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
classifier.add(Conv2D(16, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
classifier.add(Conv2D(8, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))



classifier.add(Flatten())

#hidden layer
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dropout(rate = 0.5))

#output layer
classifier.add(Dense(units = 10, activation = 'softmax'))

classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
print(classifier.summary())
#plot_model(classifier, show_shapes=True, to_file='PlantVillage_CNN.png')

#Part 2 - fitting the data set

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        'train',
        target_size=(128, 128),
        batch_size=64,
        class_mode='categorical' )
label_map = (training_set.class_indices)

print(label_map)

test_set = test_datagen.flow_from_directory(
        'val',
        target_size=(128, 128),
        batch_size=64,
        class_mode='categorical')


# Add callbacks to prevent overfitting and save time
from keras.callbacks import EarlyStopping, ModelCheckpoint

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# Save the best model during training
model_checkpoint = ModelCheckpoint(
    'tomato_disease_model_best.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

# Calculate reasonable steps per epoch (balance between speed and quality)
# Use a fraction of the dataset to speed up training while still seeing enough data
total_steps = len(training_set)
# Use 50-80 steps per epoch for faster training (adjust based on your needs)
# This is better than 20 but much faster than using the full dataset
steps_per_epoch = min(80, total_steps)  # Cap at 80 steps for speed
validation_steps = min(50, len(test_set)) if test_set else 50

print(f"Total available steps: {total_steps}")
print(f"Training with {steps_per_epoch} steps per epoch (for faster training)")
print(f"Validation with {validation_steps} steps")

classifier.fit(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=10,  # Early stopping will stop earlier if needed
        validation_data=test_set,
        validation_steps=validation_steps,
        callbacks=[early_stopping, model_checkpoint])

# Save the full model (architecture + weights) for easy loading in Streamlit
classifier.save('tomato_disease_model.h5')
print('Saved full model as tomato_disease_model.h5')

# Save class mapping to JSON file for Streamlit app
import json

# Reverse the mapping: from {class_name: index} to {index: class_name}
reverse_label_map = {v: k for k, v in label_map.items()}

with open('class_mapping.json', 'w') as f:
    json.dump(reverse_label_map, f, indent=4)

print('Saved class mapping as class_mapping.json')
print('Class mapping:', reverse_label_map)
