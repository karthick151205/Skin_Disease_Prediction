---
license: apache-2.0
---
# Skin Cancer Image Classification Model

## Introduction

This model is designed for the classification of skin cancer images into various categories including benign keratosis-like lesions, basal cell carcinoma, actinic keratoses, vascular lesions, melanocytic nevi, melanoma, and dermatofibroma.

## Model Overview

- Model Architecture: Vision Transformer (ViT)
- Pre-trained Model: Google's ViT with 16x16 patch size and trained on ImageNet21k dataset
- Modified Classification Head: The classification head has been replaced to adapt the model to the skin cancer classification task.

## Dataset

- Dataset Name: Skin Cancer Dataset
- Source: [Marmal88's Skin Cancer Dataset on Hugging Face](https://huggingface.co/datasets/marmal88/skin_cancer)
- Classes: Benign keratosis-like lesions, Basal cell carcinoma, Actinic keratoses, Vascular lesions, Melanocytic nevi, Melanoma, Dermatofibroma

## Training

- Optimizer: Adam optimizer with a learning rate of 1e-4
- Loss Function: Cross-Entropy Loss
- Batch Size: 32
- Number of Epochs: 5

## Evaluation Metrics

- Train Loss: Average loss over the training dataset
- Train Accuracy: Accuracy over the training dataset
- Validation Loss: Average loss over the validation dataset
- Validation Accuracy: Accuracy over the validation dataset

## Results

- Epoch 1/5, Train Loss: 0.7168, Train Accuracy: 0.7586, Val Loss: 0.4994, Val Accuracy: 0.8355
- Epoch 2/5, Train Loss: 0.4550, Train Accuracy: 0.8466, Val Loss: 0.3237, Val Accuracy: 0.8973
- Epoch 3/5, Train Loss: 0.2959, Train Accuracy: 0.9028, Val Loss: 0.1790, Val Accuracy: 0.9530
- Epoch 4/5, Train Loss: 0.1595, Train Accuracy: 0.9482, Val Loss: 0.1498, Val Accuracy: 0.9555
- Epoch 5/5, Train Loss: 0.1208, Train Accuracy: 0.9614, Val Loss: 0.1000, Val Accuracy: 0.9695
## Conclusion

The model demonstrates good performance in classifying skin cancer images into various categories. Further fine-tuning or experimentation may improve performance on this task.

