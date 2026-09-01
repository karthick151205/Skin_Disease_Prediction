import os
import random
import shutil

source_dir = "HAM10000_dataset"
train_dir = "HAM10000_split/train"
val_dir = "HAM10000_split/val"

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

for class_name in os.listdir(source_dir):
    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)

    images = os.listdir(os.path.join(source_dir, class_name))
    random.shuffle(images)

    split = int(0.8 * len(images))  # 80% train, 20% val

    for img in images[:split]:
        shutil.copy(
            os.path.join(source_dir, class_name, img),
            os.path.join(train_dir, class_name, img),
        )

    for img in images[split:]:
        shutil.copy(
            os.path.join(source_dir, class_name, img),
            os.path.join(val_dir, class_name, img),
        )

print("Train/Validation split completed!")