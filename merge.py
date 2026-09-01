import os
import shutil
import pandas as pd

# Paths
metadata_path = "HAM10000_metadata.csv"
image_dir_1 = "HAM10000_images_part_1"
image_dir_2 = "HAM10000_images_part_2"
output_dir = "HAM10000_dataset"

# Create output folder
os.makedirs(output_dir, exist_ok=True)

# Load metadata
df = pd.read_csv(metadata_path)

# Get unique classes
classes = df["dx"].unique()

# Create class folders
for cls in classes:
    os.makedirs(os.path.join(output_dir, cls), exist_ok=True)

# Move images to class folders
for index, row in df.iterrows():
    image_name = row["image_id"] + ".jpg"
    label = row["dx"]

    src_path1 = os.path.join(image_dir_1, image_name)
    src_path2 = os.path.join(image_dir_2, image_name)

    if os.path.exists(src_path1):
        shutil.copy(src_path1, os.path.join(output_dir, label, image_name))
    elif os.path.exists(src_path2):
        shutil.copy(src_path2, os.path.join(output_dir, label, image_name))

print("Dataset organized successfully!")