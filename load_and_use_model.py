#!/usr/bin/env python3
"""
Script para cargar y usar modelos de IA desde checkpoints (.pth)

Este script muestra cómo:
1. Cargar un checkpoint
2. Reconstruir el modelo
3. Hacer predicciones con el modelo
"""

import torch
import torch.nn as nn
import numpy as np
from PIL import Image
import torchvision.transforms as transforms


# ============================================================================
# EJEMPLO 1: Definir arquitectura del modelo
# ============================================================================
# IMPORTANTE: Debes conocer la arquitectura original del modelo
# Aquí hay ejemplos comunes para modelos de visión por computadora

class SimpleUNet(nn.Module):
    """
    Ejemplo de arquitectura U-Net para segmentación de imágenes
    (común en aplicaciones médicas como segmentación de disco óptico)
    """
    def __init__(self, in_channels=3, out_channels=1):
        super(SimpleUNet, self).__init__()

        # Encoder (downsampling)
        self.enc1 = self.conv_block(in_channels, 64)
        self.enc2 = self.conv_block(64, 128)
        self.enc3 = self.conv_block(128, 256)
        self.enc4 = self.conv_block(256, 512)

        # Bottleneck
        self.bottleneck = self.conv_block(512, 1024)

        # Decoder (upsampling)
        self.upconv4 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.dec4 = self.conv_block(1024, 512)

        self.upconv3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = self.conv_block(512, 256)

        self.upconv2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = self.conv_block(256, 128)

        self.upconv1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = self.conv_block(128, 64)

        # Output
        self.out = nn.Conv2d(64, out_channels, 1)

        self.pool = nn.MaxPool2d(2, 2)

    def conv_block(self, in_ch, out_ch):
        return nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        # Encoder
        enc1 = self.enc1(x)
        enc2 = self.enc2(self.pool(enc1))
        enc3 = self.enc3(self.pool(enc2))
        enc4 = self.enc4(self.pool(enc3))

        # Bottleneck
        bottleneck = self.bottleneck(self.pool(enc4))

        # Decoder with skip connections
        dec4 = self.upconv4(bottleneck)
        dec4 = torch.cat([dec4, enc4], dim=1)
        dec4 = self.dec4(dec4)

        dec3 = self.upconv3(dec4)
        dec3 = torch.cat([dec3, enc3], dim=1)
        dec3 = self.dec3(dec3)

        dec2 = self.upconv2(dec3)
        dec2 = torch.cat([dec2, enc2], dim=1)
        dec2 = self.dec2(dec2)

        dec1 = self.upconv1(dec2)
        dec1 = torch.cat([dec1, enc1], dim=1)
        dec1 = self.dec1(dec1)

        return torch.sigmoid(self.out(dec1))


class SimpleCNN(nn.Module):
    """
    Ejemplo de CNN simple para clasificación
    """
    def __init__(self, num_classes=2):
        super(SimpleCNN, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )

        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# ============================================================================
# EJEMPLO 2: Cargar checkpoint
# ============================================================================

def load_checkpoint(checkpoint_path, model, device='cpu'):
    """
    Carga un checkpoint y lo aplica al modelo

    Args:
        checkpoint_path: Ruta al archivo .pth
        model: Instancia del modelo (debe coincidir con la arquitectura)
        device: 'cpu' o 'cuda'

    Returns:
        model: Modelo con pesos cargados
        checkpoint: Diccionario con información adicional
    """
    print(f"Cargando checkpoint desde: {checkpoint_path}")

    # Cargar checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device)

    # Extraer state_dict
    if isinstance(checkpoint, dict):
        if 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        elif 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        else:
            # El checkpoint puede ser directamente el state_dict
            state_dict = checkpoint
    else:
        state_dict = checkpoint.state_dict()

    # Cargar pesos en el modelo
    try:
        model.load_state_dict(state_dict)
        print("✓ Pesos cargados exitosamente")
    except Exception as e:
        print(f"⚠ Advertencia al cargar pesos: {e}")
        print("  Intentando carga flexible...")
        model.load_state_dict(state_dict, strict=False)

    # Poner modelo en modo evaluación
    model.eval()

    return model, checkpoint


# ============================================================================
# EJEMPLO 3: Hacer predicciones
# ============================================================================

def predict_segmentation(model, image_path, device='cpu'):
    """
    Hace predicción de segmentación en una imagen

    Args:
        model: Modelo cargado
        image_path: Ruta a la imagen de entrada
        device: 'cpu' o 'cuda'

    Returns:
        mask: Máscara de segmentación predicha
    """
    # Cargar y preprocesar imagen
    image = Image.open(image_path).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Ajustar según tu modelo
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

    image_tensor = transform(image).unsqueeze(0).to(device)

    # Predicción
    with torch.no_grad():
        output = model(image_tensor)

    # Post-procesamiento
    mask = output.squeeze().cpu().numpy()
    mask = (mask > 0.5).astype(np.uint8) * 255  # Binarizar

    return mask


def predict_classification(model, image_path, class_names, device='cpu'):
    """
    Hace predicción de clasificación en una imagen

    Args:
        model: Modelo cargado
        image_path: Ruta a la imagen de entrada
        class_names: Lista con nombres de clases
        device: 'cpu' o 'cuda'

    Returns:
        predicted_class: Clase predicha
        confidence: Confianza de la predicción
    """
    # Cargar y preprocesar imagen
    image = Image.open(image_path).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

    image_tensor = transform(image).unsqueeze(0).to(device)

    # Predicción
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)

    # Obtener clase con mayor probabilidad
    confidence, predicted_idx = torch.max(probabilities, 1)

    predicted_class = class_names[predicted_idx.item()]
    confidence = confidence.item()

    return predicted_class, confidence


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def main():
    """
    Ejemplo de uso completo
    """
    print("="*70)
    print("EJEMPLO: Cargar y usar modelo desde checkpoint")
    print("="*70)

    # Configuración
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nUsando dispositivo: {device}")

    # =========================================================================
    # OPCIÓN 1: Modelo de segmentación (U-Net)
    # =========================================================================
    print("\n--- Ejemplo 1: Modelo de Segmentación ---")

    # Crear modelo
    model_seg = SimpleUNet(in_channels=3, out_channels=1)
    model_seg = model_seg.to(device)

    print(f"Modelo creado: {model_seg.__class__.__name__}")
    print(f"Parámetros totales: {sum(p.numel() for p in model_seg.parameters()):,}")

    # Para cargar checkpoint (descomentary ajustar ruta):
    # model_seg, checkpoint = load_checkpoint('checkpoint.pth', model_seg, device)
    #
    # Para hacer predicción:
    # mask = predict_segmentation(model_seg, 'imagen_ojo.jpg', device)
    # Image.fromarray(mask).save('mascara_predicha.png')

    # =========================================================================
    # OPCIÓN 2: Modelo de clasificación
    # =========================================================================
    print("\n--- Ejemplo 2: Modelo de Clasificación ---")

    # Crear modelo
    model_clf = SimpleCNN(num_classes=2)
    model_clf = model_clf.to(device)

    print(f"Modelo creado: {model_clf.__class__.__name__}")
    print(f"Parámetros totales: {sum(p.numel() for p in model_clf.parameters()):,}")

    # Para cargar checkpoint:
    # model_clf, checkpoint = load_checkpoint('checkpoint.pth', model_clf, device)
    #
    # Para hacer predicción:
    # class_names = ['Normal', 'Glaucoma']
    # predicted, confidence = predict_classification(
    #     model_clf, 'imagen_ojo.jpg', class_names, device
    # )
    # print(f"Predicción: {predicted} (confianza: {confidence:.2%})")

    print("\n" + "="*70)
    print("INSTRUCCIONES:")
    print("="*70)
    print("\n1. Primero ejecuta 'extract_model_info.py' para analizar tu checkpoint")
    print("2. Identifica la arquitectura del modelo")
    print("3. Define la clase del modelo en este archivo")
    print("4. Descomentar las líneas para cargar el checkpoint")
    print("5. Hacer predicciones con tus imágenes")
    print("\n")


if __name__ == '__main__':
    main()
