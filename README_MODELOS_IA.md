# Extracción de Modelos IA - Proyecto ModeloIA

## 📋 Resumen

Este proyecto proporciona herramientas para extraer, analizar y usar modelos de IA almacenados en archivos checkpoint de PyTorch (`.pth`).

Los archivos checkpoint que tienes (`checkpoint.pth` y `checkpointMask.pth`) contienen modelos de deep learning entrenados, probablemente para:

- **Segmentación de disco óptico/copa óptica** (detección de glaucoma)
- **Clasificación de patologías oculares**
- **Detección de drusas u otras anomalías**

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements_pytorch.txt
```

### 2. Colocar los Archivos Checkpoint

Coloca `checkpoint.pth` y `checkpointMask.pth` en el directorio raíz del proyecto:

```
ModeloIA/
├── checkpoint.pth           # ← Coloca aquí
├── checkpointMask.pth       # ← Coloca aquí
├── extract_model_info.py
└── ...
```

### 3. Análisis Rápido

```bash
python quick_start.py
```

### 4. Análisis Detallado

```bash
python extract_model_info.py checkpoint.pth
python extract_model_info.py checkpointMask.pth
```

## 📂 Archivos Incluidos

| Archivo | Descripción |
|---------|-------------|
| `quick_start.py` | Script de inicio rápido para análisis básico |
| `extract_model_info.py` | Herramienta completa de análisis de checkpoints |
| `load_and_use_model.py` | Ejemplos de cómo cargar y usar los modelos |
| `GUIA_EXTRACCION_MODELO.md` | Guía completa paso a paso |
| `requirements_pytorch.txt` | Dependencias necesarias |

## 🔍 ¿Qué Hacen los Scripts?

### quick_start.py
- ✓ Verifica dependencias
- ✓ Busca archivos .pth automáticamente
- ✓ Muestra análisis básico de cada checkpoint
- ✓ Identifica el tipo de modelo

**Ejemplo de salida:**
```
Analizando: checkpoint.pth
✓ Encontrado 'state_dict' con 156 tensores
  Parámetros totales: 31,042,592

  Componentes detectados:
    - CNN (Convolucional)
    - Batch Normalization
    - Decoder/Upsampling (posible U-Net)
```

### extract_model_info.py
- ✓ Análisis profundo de la arquitectura
- ✓ Lista todas las capas del modelo
- ✓ Calcula número de parámetros
- ✓ Identifica tipo de red (U-Net, ResNet, etc.)
- ✓ Extrae hiperparámetros y métricas
- ✓ Genera archivos de resumen

**Archivos generados:**
- `checkpoint_summary.json` - Resumen estructurado
- `checkpoint_architecture.txt` - Arquitectura detallada

### load_and_use_model.py
- ✓ Ejemplos de arquitecturas comunes (U-Net, CNN)
- ✓ Funciones para cargar checkpoints
- ✓ Funciones para hacer predicciones
- ✓ Código listo para adaptar

## 📖 Guía Completa

Para instrucciones detalladas, consulta:

👉 **[GUIA_EXTRACCION_MODELO.md](GUIA_EXTRACCION_MODELO.md)**

Esta guía incluye:

- Conceptos básicos de checkpoints PyTorch
- Interpretación de arquitecturas
- Reconstrucción de modelos
- Integración con el proyecto Django actual
- Troubleshooting y soluciones a errores comunes

## 🎯 Flujo de Trabajo Recomendado

```
1. Instalar dependencias
   ↓
2. Ejecutar quick_start.py
   ↓
3. Ejecutar extract_model_info.py para análisis detallado
   ↓
4. Revisar los archivos generados (*_summary.json, *_architecture.txt)
   ↓
5. Identificar la arquitectura del modelo
   ↓
6. Definir la clase del modelo en Python
   ↓
7. Cargar checkpoint con load_and_use_model.py
   ↓
8. Hacer predicciones con imágenes de prueba
   ↓
9. (Opcional) Integrar con el backend Django
```

## 💡 Casos de Uso

### Caso 1: Solo quiero ver qué contiene el checkpoint

```bash
python quick_start.py
```

### Caso 2: Necesito información detallada del modelo

```bash
python extract_model_info.py checkpoint.pth
# Revisar los archivos generados
cat checkpoint_summary.json
cat checkpoint_architecture.txt
```

### Caso 3: Quiero usar el modelo para hacer predicciones

1. Ejecutar análisis detallado
2. Identificar arquitectura
3. Editar `load_and_use_model.py` con la arquitectura correcta
4. Cargar checkpoint y hacer predicciones

```python
# Ejemplo en load_and_use_model.py
model = UNetSegmentation()
checkpoint = torch.load('checkpoint.pth', map_location='cpu')
model.load_state_dict(checkpoint['state_dict'])
model.eval()

# Hacer predicción
mask = predict_segmentation(model, 'imagen_ojo.jpg')
```

## 🔗 Integración con Proyecto Actual

El proyecto actual usa procesamiento de imágenes tradicional con OpenCV:

- `disco_optico/views.py` - Detección de glaucoma con algoritmos clásicos
- `drusas/views.py` - Conversión a espacio de color HSV

Para integrar los modelos PyTorch:

### Opción 1: Reemplazar algoritmo actual

Modifica `disco_optico/views.py` para usar el modelo PyTorch en lugar de OpenCV.

### Opción 2: Crear nuevos endpoints

Añade nuevas vistas que usen los modelos de IA:

```python
# disco_optico/urls.py
urlpatterns = [
    path('segment-ai/', OpticDiscSegmentationAI.as_view()),
    path('classify-glaucoma-ai/', GlaucomaClassificationAI.as_view()),
]
```

Ver `GUIA_EXTRACCION_MODELO.md` para ejemplos completos.

## ⚠️ Notas Importantes

1. **Los archivos .pth NO están en este repositorio**
   - Debes obtenerlos del autor original del modelo
   - Colócalos en la raíz del proyecto antes de ejecutar los scripts

2. **Necesitas conocer la arquitectura del modelo**
   - Los scripts te ayudan a identificarla
   - Pero necesitas el código original o reconstruirla manualmente

3. **El proyecto actual NO usa PyTorch**
   - Usa OpenCV y algoritmos tradicionales
   - Los checkpoints .pth son un desarrollo aparte
   - Puedes integrarlos si lo deseas

## 🆘 Solución de Problemas

### "No se encontraron archivos .pth"

Coloca `checkpoint.pth` y `checkpointMask.pth` en el directorio raíz.

### "ModuleNotFoundError: No module named 'torch'"

```bash
pip install torch torchvision
```

### "RuntimeError: Error(s) in loading state_dict"

La arquitectura del modelo no coincide. Revisa:
- Número de canales de entrada/salida
- Número de clases (para clasificación)
- Dimensiones de las capas

### "CUDA out of memory"

Carga el modelo en CPU:

```python
checkpoint = torch.load('checkpoint.pth', map_location=torch.device('cpu'))
```

## 📚 Recursos Adicionales

- [PyTorch Documentation](https://pytorch.org/docs/)
- [Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [U-Net Paper](https://arxiv.org/abs/1505.04597)
- [Medical Image Segmentation with PyTorch](https://github.com/mateuszbuda/brain-segmentation-pytorch)

## 🤝 Contribuir

Si encuentras errores o mejoras:

1. Reporta issues en el repositorio
2. Envía pull requests con mejoras
3. Comparte tus resultados

## 📝 Licencia

Este código es de uso educativo y de investigación.

---

**¿Necesitas ayuda?**

1. Revisa `GUIA_EXTRACCION_MODELO.md`
2. Ejecuta `python quick_start.py` para diagnóstico
3. Revisa los archivos generados por `extract_model_info.py`

**Versión:** 1.0
**Última actualización:** 2025-11-11
