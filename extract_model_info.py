#!/usr/bin/env python3
"""
Script para extraer y analizar modelos de IA desde archivos checkpoint (.pth)

Uso:
    python extract_model_info.py checkpoint.pth
    python extract_model_info.py checkpointMask.pth
"""

import torch
import sys
import json
from pathlib import Path


def analyze_checkpoint(checkpoint_path):
    """Analiza un archivo checkpoint de PyTorch"""

    print(f"\n{'='*70}")
    print(f"Analizando: {checkpoint_path}")
    print(f"{'='*70}\n")

    try:
        # Cargar el checkpoint
        # Si el checkpoint fue entrenado en GPU pero estás en CPU, usa map_location
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))

        print(f"✓ Checkpoint cargado exitosamente\n")

        # Tipo de objeto
        print(f"Tipo de checkpoint: {type(checkpoint)}\n")

        # Analizar según el tipo
        if isinstance(checkpoint, dict):
            analyze_dict_checkpoint(checkpoint)
        elif hasattr(checkpoint, 'state_dict'):
            analyze_model_checkpoint(checkpoint)
        else:
            print("Estructura del checkpoint:")
            print(f"  Tipo: {type(checkpoint)}")
            if hasattr(checkpoint, '__dict__'):
                print(f"  Atributos: {list(checkpoint.__dict__.keys())}")

        return checkpoint

    except Exception as e:
        print(f"✗ Error al cargar checkpoint: {e}")
        return None


def analyze_dict_checkpoint(checkpoint):
    """Analiza un checkpoint en formato diccionario"""

    print("Claves principales del checkpoint:")
    for key in checkpoint.keys():
        print(f"  - {key}")
    print()

    # Analizar state_dict si existe
    if 'state_dict' in checkpoint:
        print("\n--- STATE DICT (Pesos del Modelo) ---")
        analyze_state_dict(checkpoint['state_dict'])
    elif 'model_state_dict' in checkpoint:
        print("\n--- MODEL STATE DICT (Pesos del Modelo) ---")
        analyze_state_dict(checkpoint['model_state_dict'])
    else:
        # El checkpoint puede ser directamente el state_dict
        print("\n--- Analizando como STATE DICT directo ---")
        analyze_state_dict(checkpoint)

    # Mostrar otra información disponible
    if 'epoch' in checkpoint:
        print(f"\nÉpoca de entrenamiento: {checkpoint['epoch']}")

    if 'optimizer_state_dict' in checkpoint:
        print(f"\n✓ Incluye estado del optimizador")

    if 'loss' in checkpoint:
        print(f"\nPérdida (loss): {checkpoint['loss']}")

    if 'accuracy' in checkpoint:
        print(f"Precisión (accuracy): {checkpoint['accuracy']}")

    # Buscar hiperparámetros
    hyperparams_keys = ['learning_rate', 'lr', 'batch_size', 'num_epochs',
                       'model_name', 'architecture', 'config']
    found_hyperparams = {k: checkpoint[k] for k in hyperparams_keys if k in checkpoint}

    if found_hyperparams:
        print("\n--- Hiperparámetros ---")
        for key, value in found_hyperparams.items():
            print(f"  {key}: {value}")


def analyze_state_dict(state_dict):
    """Analiza el state_dict del modelo"""

    print(f"Número total de tensores: {len(state_dict)}\n")

    # Agrupar por capas
    layers = {}
    total_params = 0

    for key, tensor in state_dict.items():
        layer_name = key.rsplit('.', 1)[0]  # Nombre sin .weight o .bias

        if layer_name not in layers:
            layers[layer_name] = {'params': [], 'shapes': []}

        layers[layer_name]['params'].append(key)
        layers[layer_name]['shapes'].append(tuple(tensor.shape))

        # Contar parámetros
        total_params += tensor.numel()

    print(f"Parámetros totales: {total_params:,}\n")

    print("Arquitectura del modelo (capas detectadas):")
    for i, (layer_name, info) in enumerate(layers.items(), 1):
        print(f"\n  {i}. {layer_name}")
        for param, shape in zip(info['params'], info['shapes']):
            print(f"     - {param.split('.')[-1]}: {shape}")

    # Identificar tipo de red
    print("\n--- Análisis de Arquitectura ---")
    identify_architecture(state_dict)


def identify_architecture(state_dict):
    """Intenta identificar el tipo de arquitectura de red"""

    keys = list(state_dict.keys())

    architectures = []

    # Detectar convolucionales
    if any('conv' in k.lower() for k in keys):
        architectures.append("Red Convolucional (CNN)")

    # Detectar batch normalization
    if any('bn' in k.lower() or 'batch_norm' in k.lower() for k in keys):
        architectures.append("Usa Batch Normalization")

    # Detectar LSTM/GRU
    if any('lstm' in k.lower() for k in keys):
        architectures.append("LSTM (Recurrente)")
    if any('gru' in k.lower() for k in keys):
        architectures.append("GRU (Recurrente)")

    # Detectar atención/transformers
    if any('attention' in k.lower() or 'attn' in k.lower() for k in keys):
        architectures.append("Mecanismo de Atención")

    # Detectar capas fully connected
    if any('fc' in k.lower() or 'linear' in k.lower() for k in keys):
        architectures.append("Capas Fully Connected")

    if architectures:
        print("Componentes detectados:")
        for arch in architectures:
            print(f"  - {arch}")
    else:
        print("  No se pudo identificar automáticamente la arquitectura")


def save_checkpoint_summary(checkpoint_path, checkpoint):
    """Guarda un resumen del checkpoint en formato JSON"""

    summary = {
        'checkpoint_file': str(checkpoint_path),
        'type': str(type(checkpoint)),
    }

    if isinstance(checkpoint, dict):
        summary['keys'] = list(checkpoint.keys())

        state_dict_key = None
        if 'state_dict' in checkpoint:
            state_dict_key = 'state_dict'
        elif 'model_state_dict' in checkpoint:
            state_dict_key = 'model_state_dict'

        if state_dict_key:
            state_dict = checkpoint[state_dict_key]
            summary['layers'] = list(state_dict.keys())
            summary['total_parameters'] = sum(t.numel() for t in state_dict.values())

    output_file = Path(checkpoint_path).stem + '_summary.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Resumen guardado en: {output_file}")


def export_model_architecture(checkpoint, output_file='model_architecture.txt'):
    """Exporta la arquitectura del modelo a un archivo de texto"""

    with open(output_file, 'w', encoding='utf-8') as f:
        if isinstance(checkpoint, dict):
            state_dict = checkpoint.get('state_dict', checkpoint.get('model_state_dict', checkpoint))
        else:
            state_dict = checkpoint.state_dict() if hasattr(checkpoint, 'state_dict') else {}

        f.write("ARQUITECTURA DEL MODELO\n")
        f.write("=" * 70 + "\n\n")

        for key, tensor in state_dict.items():
            f.write(f"{key}\n")
            f.write(f"  Shape: {tuple(tensor.shape)}\n")
            f.write(f"  Parámetros: {tensor.numel():,}\n")
            f.write(f"  Dtype: {tensor.dtype}\n\n")

    print(f"✓ Arquitectura exportada a: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python extract_model_info.py <checkpoint.pth>")
        print("\nEjemplos:")
        print("  python extract_model_info.py checkpoint.pth")
        print("  python extract_model_info.py checkpointMask.pth")
        sys.exit(1)

    checkpoint_path = sys.argv[1]

    if not Path(checkpoint_path).exists():
        print(f"✗ Error: El archivo '{checkpoint_path}' no existe")
        sys.exit(1)

    # Analizar checkpoint
    checkpoint = analyze_checkpoint(checkpoint_path)

    if checkpoint is not None:
        # Guardar resumen
        save_checkpoint_summary(checkpoint_path, checkpoint)

        # Exportar arquitectura
        output_arch = Path(checkpoint_path).stem + '_architecture.txt'
        export_model_architecture(checkpoint, output_arch)

        print(f"\n{'='*70}")
        print("Análisis completado exitosamente")
        print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
