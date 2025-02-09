import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os
from PIL import Image
import numpy as np

def is_valid_image(file_path):
    """Check if the file is a valid image (JPEG, PNG, or BMP)."""
    try:
        with Image.open(file_path) as img:
            # Check if the format is supported
            if img.format not in ['JPEG', 'PNG', 'BMP']:
                return False
            return True
    except:
        return False

def prepare_dataset(directory, batch_size=32, img_size=(224, 224)):
    """Load and prepare dataset, filtering out invalid images."""
    
    # First, validate and filter images
    valid_images = []
    valid_labels = []
    class_names = sorted(os.listdir(directory))
    class_to_label = {class_name: i for i, class_name in enumerate(class_names)}
    
    print(f"\nProcessing directory: {directory}")
    print("Found classes:", class_names)
    
    for class_name in class_names:
        class_dir = os.path.join(directory, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        for img_name in os.listdir(class_dir):
            img_path = os.path.join(class_dir, img_name)
            if is_valid_image(img_path):
                valid_images.append(img_path)
                valid_labels.append(class_to_label[class_name])
            else:
                print(f"❌ Skipping invalid image: {img_path}")
    
    print(f"✅ Found {len(valid_images)} valid images")
    
    # Create dataset
    dataset = tf.data.Dataset.from_tensor_slices((valid_images, valid_labels))
    
    def load_and_preprocess(img_path, label):
        # Read image file
        img = tf.io.read_file(img_path)
        # Decode image
        img = tf.image.decode_jpeg(img, channels=3)
        # Resize
        img = tf.image.resize(img, img_size)
        # Normalize
        img = tf.cast(img, tf.float32) / 255.0
        return img, label
    
    # Transform dataset
    dataset = dataset.map(load_and_preprocess)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    if 'train' in directory.lower():
        dataset = dataset.shuffle(buffer_size=1000)
        
    return dataset

# Define paths
train_path = "models/train"
val_path = "models/val"
test_path = "models/test"

# Load datasets
batch_size = 32
img_size = (224, 224)

print("Loading datasets...")
train_dataset = prepare_dataset(train_path, batch_size, img_size)
val_dataset = prepare_dataset(val_path, batch_size, img_size)
test_dataset = prepare_dataset(test_path, batch_size, img_size)

# Create model
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(3, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=x)

# Compile model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Add callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2
    )
]

# Train model
epochs = 5
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=epochs,
    callbacks=callbacks
)

# Evaluate
test_loss, test_acc = model.evaluate(test_dataset)
print(f"\n🎯 Test Accuracy: {test_acc:.2%}")

test_loss, test_acc = model.evaluate(test_dataset)
print(f"\n🎯 Test Accuracy: {test_acc:.2%}")

# Save the final model
model.save("final_model")