# Guía de Extracción y Uso de Modelos IA

## Introducción

Esta guía te explica cómo extraer, analizar y usar los modelos de IA contenidos en los archivos checkpoint que te proporcionaron:

- `checkpoint.pth`
- `checkpointMask.pth`

## ¿Qué son los archivos .pth?

Los archivos `.pth` (PyTorch) son checkpoints que guardan el estado de un modelo entrenado. Típicamente contienen:

- **state_dict**: Pesos y parámetros del modelo (lo más importante)
- **optimizer_state_dict**: Estado del optimizador (para continuar entrenamiento)
- **epoch**: Época de entrenamiento en la que se guardó
- **loss/accuracy**: Métricas de rendimiento
- **hyperparameters**: Hiperparámetros usados en el entrenamiento

## Estructura del Proyecto

```
ModeloIA/
├── checkpoint.pth                      # Checkpoint del modelo principal
├── checkpointMask.pth                  # Checkpoint del modelo de máscara
├── extract_model_info.py              # Script para analizar checkpoints
├── load_and_use_model.py              # Script para cargar y usar modelos
└── GUIA_EXTRACCION_MODELO.md          # Esta guía
```

## Paso 1: Instalar Dependencias

Primero, instala PyTorch:

```bash
# Para CPU
pip install torch torchvision

# Para GPU (CUDA 11.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Dependencias adicionales
pip install numpy pillow matplotlib
```

## Paso 2: Analizar los Checkpoints

Usa el script `extract_model_info.py` para inspeccionar el contenido de los checkpoints:

```bash
# Analizar checkpoint principal
python extract_model_info.py checkpoint.pth

# Analizar checkpoint de máscara
python extract_model_info.py checkpointMask.pth
```

Este script te mostrará:

- ✓ Tipo de checkpoint
- ✓ Claves principales (epoch, state_dict, optimizer, etc.)
- ✓ Arquitectura del modelo (capas, tipos de capas)
- ✓ Número total de parámetros
- ✓ Tipo de red neural (CNN, U-Net, etc.)

**Salidas generadas:**

- `checkpoint_summary.json` - Resumen en formato JSON
- `checkpoint_architecture.txt` - Arquitectura detallada del modelo

## Paso 3: Interpretar la Arquitectura

Después de ejecutar el script, revisa la salida para identificar:

### Modelos Comunes en Aplicaciones Médicas

| Patrón Detectado | Tipo de Modelo | Uso Común |
|-----------------|----------------|-----------|
| Convoluciones + Encoder-Decoder | **U-Net** | Segmentación de imágenes médicas |
| Conv2d + MaxPool + Linear | **CNN Clasificador** | Diagnóstico/Clasificación |
| ResNet blocks | **ResNet** | Transfer learning |
| Atención/Transformers | **Vision Transformer** | Análisis avanzado de imágenes |

### Ejemplo de Salida

```
Arquitectura del modelo (capas detectadas):

  1. encoder.conv1
     - weight: (64, 3, 3, 3)
     - bias: (64,)

  2. encoder.bn1
     - weight: (64,)
     - bias: (64,)

  ...

Componentes detectados:
  - Red Convolucional (CNN)
  - Usa Batch Normalization
  - Capas Fully Connected
```

## Paso 4: Reconstruir el Modelo

Una vez identificada la arquitectura, debes definir el modelo en Python.

### Opción A: Arquitectura Conocida (U-Net para Segmentación)

Si los checkpoints son para segmentación de disco óptico/glaucoma:

```python
import torch
import torch.nn as nn

class UNetSegmentation(nn.Module):
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()
        # ... ver load_and_use_model.py
```

### Opción B: Arquitectura Desconocida

Si no conoces la arquitectura original:

1. **Buscar el código fuente**: Los checkpoints suelen venir con el código del modelo
2. **Ingeniería inversa**: Usa la información de `extract_model_info.py` para reconstruir
3. **Contactar al autor**: Pregunta por el código del modelo

## Paso 5: Cargar los Pesos del Modelo

```python
import torch

# 1. Definir el modelo (debe coincidir con la arquitectura original)
model = UNetSegmentation(in_channels=3, out_channels=1)

# 2. Cargar el checkpoint
checkpoint = torch.load('checkpoint.pth', map_location='cpu')

# 3. Extraer el state_dict
if 'state_dict' in checkpoint:
    state_dict = checkpoint['state_dict']
else:
    state_dict = checkpoint

# 4. Cargar pesos en el modelo
model.load_state_dict(state_dict)

# 5. Poner en modo evaluación
model.eval()

print("✓ Modelo cargado exitosamente")
```

## Paso 6: Usar el Modelo para Predicciones

### Ejemplo: Segmentación de Imágenes Médicas

```python
from PIL import Image
import torchvision.transforms as transforms
import numpy as np

def predict(model, image_path):
    # Cargar imagen
    image = Image.open(image_path).convert('RGB')

    # Preprocesamiento
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    # Convertir a tensor
    input_tensor = transform(image).unsqueeze(0)

    # Predicción
    with torch.no_grad():
        output = model(input_tensor)

    # Post-procesamiento
    mask = output.squeeze().numpy()
    mask = (mask > 0.5).astype(np.uint8) * 255

    return mask

# Uso
mask = predict(model, 'imagen_fondo_ojo.jpg')
Image.fromarray(mask).save('segmentacion_predicha.png')
```

## Diferencia entre checkpoint.pth y checkpointMask.pth

Probablemente:

- **checkpoint.pth**: Modelo principal (clasificación de glaucoma o detección de anomalías)
- **checkpointMask.pth**: Modelo de segmentación (genera máscaras del disco óptico/copa óptica)

Para confirmar, ejecuta `extract_model_info.py` en ambos y compara:

- Número de capas
- Tipo de salida (clasificación vs segmentación)
- Tamaño de los parámetros

## Integración con el Proyecto Actual

El proyecto actual (`disco_optico` y `drusas`) usa **OpenCV tradicional**. Para integrar los modelos PyTorch:

### Opción 1: Reemplazar el algoritmo actual

```python
# En disco_optico/views.py
import torch
from .models_ml import load_optic_disc_model, predict_segmentation

class ImageViewSet(viewsets.ModelViewSet):
    def create(self, request):
        # ... código actual ...

        # Reemplazar algoritmo de OpenCV por modelo PyTorch
        model = load_optic_disc_model('checkpoint.pth')
        mask = predict_segmentation(model, image)

        # Continuar con el resto del pipeline
        # ...
```

### Opción 2: Crear endpoints nuevos

```python
# En disco_optico/urls.py
urlpatterns = [
    path('segment-ai/', ImageSegmentationAI.as_view()),
    path('classify-ai/', ImageClassificationAI.as_view()),
]
```

## Troubleshooting

### Error: "Can't find state_dict"

```python
# Inspeccionar el checkpoint
checkpoint = torch.load('checkpoint.pth')
print(checkpoint.keys())  # Ver qué claves tiene
```

### Error: "Size mismatch"

La arquitectura del modelo no coincide. Revisa:

- Número de canales de entrada/salida
- Dimensiones de las capas
- Número de clases (para clasificación)

### Error: "CUDA out of memory"

```python
# Cargar en CPU
checkpoint = torch.load('checkpoint.pth', map_location=torch.device('cpu'))
```

## Recursos Adicionales

- **PyTorch Docs**: https://pytorch.org/docs/stable/index.html
- **U-Net Paper**: https://arxiv.org/abs/1505.04597
- **Transfer Learning**: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

## Scripts Incluidos

### 1. extract_model_info.py

**Propósito**: Analizar checkpoints y extraer información

**Uso**:
```bash
python extract_model_info.py checkpoint.pth
```

**Salida**:
- Información en consola
- `checkpoint_summary.json`
- `checkpoint_architecture.txt`

### 2. load_and_use_model.py

**Propósito**: Ejemplos de cómo cargar y usar modelos

**Incluye**:
- Definiciones de arquitecturas comunes (U-Net, CNN)
- Funciones para cargar checkpoints
- Funciones para hacer predicciones
- Ejemplos completos de uso

## Próximos Pasos

1. ✓ Ejecutar `extract_model_info.py` en ambos checkpoints
2. ✓ Analizar la arquitectura detectada
3. ⬜ Definir las clases del modelo en Python
4. ⬜ Cargar los checkpoints
5. ⬜ Probar predicciones con imágenes de prueba
6. ⬜ Integrar con el backend Django (opcional)

## Soporte

Si necesitas ayuda adicional:

1. Revisa los archivos generados por `extract_model_info.py`
2. Comparte la salida del análisis para obtener ayuda específica
3. Busca si tienes documentación o código fuente original del modelo

---

**Nota**: Esta guía asume que tienes acceso a los archivos `checkpoint.pth` y `checkpointMask.pth`. Colócalos en la raíz del proyecto antes de ejecutar los scripts.
