#!/usr/bin/env python3
"""
INICIO RÁPIDO: Analizar checkpoints de modelos PyTorch

Este script proporciona una forma rápida de comenzar a trabajar con
los archivos checkpoint.pth y checkpointMask.pth

Uso:
    python quick_start.py
"""

import os
import sys
from pathlib import Path


def check_dependencies():
    """Verifica que las dependencias necesarias estén instaladas"""
    print("Verificando dependencias...\n")

    dependencies = {
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'PIL': 'Pillow',
        'numpy': 'NumPy'
    }

    missing = []

    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} instalado")
        except ImportError:
            print(f"✗ {name} NO instalado")
            missing.append(name)

    if missing:
        print(f"\n⚠ Faltan dependencias: {', '.join(missing)}")
        print("\nInstala con:")
        print("  pip install -r requirements_pytorch.txt")
        print("\nO manualmente:")
        print("  pip install torch torchvision pillow numpy")
        return False

    print("\n✓ Todas las dependencias están instaladas\n")
    return True


def find_checkpoints():
    """Busca archivos .pth en el directorio actual"""
    print("Buscando archivos checkpoint (.pth)...\n")

    pth_files = list(Path('.').glob('*.pth'))

    if not pth_files:
        print("⚠ No se encontraron archivos .pth en el directorio actual")
        print("\nColoca los archivos checkpoint.pth y checkpointMask.pth aquí:")
        print(f"  {Path.cwd()}\n")
        return []

    print("Archivos encontrados:")
    for i, file in enumerate(pth_files, 1):
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  {i}. {file.name} ({size_mb:.2f} MB)")

    print()
    return pth_files


def analyze_checkpoint(checkpoint_path):
    """Análisis básico de un checkpoint"""
    import torch

    print(f"\n{'='*70}")
    print(f"Analizando: {checkpoint_path.name}")
    print(f"{'='*70}\n")

    try:
        # Cargar checkpoint
        checkpoint = torch.load(checkpoint_path, map_location='cpu')

        # Información básica
        print(f"Tipo: {type(checkpoint)}")

        if isinstance(checkpoint, dict):
            print(f"\nClaves del checkpoint:")
            for key in checkpoint.keys():
                if isinstance(checkpoint[key], dict):
                    print(f"  - {key}: {len(checkpoint[key])} elementos")
                elif hasattr(checkpoint[key], 'shape'):
                    print(f"  - {key}: shape {checkpoint[key].shape}")
                else:
                    print(f"  - {key}: {checkpoint[key]}")

            # Buscar state_dict
            state_dict = None
            if 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
                print(f"\n✓ Encontrado 'state_dict' con {len(state_dict)} tensores")
            elif 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
                print(f"\n✓ Encontrado 'model_state_dict' con {len(state_dict)} tensores")
            else:
                # El checkpoint puede ser directamente el state_dict
                if all(isinstance(v, torch.Tensor) for v in checkpoint.values()):
                    state_dict = checkpoint
                    print(f"\n✓ El checkpoint es directamente un state_dict con {len(state_dict)} tensores")

            # Contar parámetros
            if state_dict:
                total_params = sum(t.numel() for t in state_dict.values())
                print(f"  Parámetros totales: {total_params:,}")

                # Mostrar primeras capas
                print(f"\n  Primeras 5 capas:")
                for i, (key, tensor) in enumerate(list(state_dict.items())[:5], 1):
                    print(f"    {i}. {key}: {tuple(tensor.shape)}")

                # Identificar tipo de modelo
                keys_str = ' '.join(state_dict.keys())
                model_type = []

                if 'conv' in keys_str.lower():
                    model_type.append("CNN (Convolucional)")
                if 'bn' in keys_str.lower() or 'batch_norm' in keys_str.lower():
                    model_type.append("Batch Normalization")
                if 'fc' in keys_str.lower() or 'linear' in keys_str.lower():
                    model_type.append("Fully Connected")
                if 'upconv' in keys_str.lower() or 'upsample' in keys_str.lower():
                    model_type.append("Decoder/Upsampling (posible U-Net)")

                if model_type:
                    print(f"\n  Componentes detectados:")
                    for comp in model_type:
                        print(f"    - {comp}")

        print(f"\n✓ Análisis completado\n")
        return True

    except Exception as e:
        print(f"\n✗ Error al analizar: {e}\n")
        return False


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("INICIO RÁPIDO - Análisis de Checkpoints PyTorch")
    print("="*70 + "\n")

    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)

    # Buscar archivos
    checkpoints = find_checkpoints()

    if not checkpoints:
        print("📝 Pasos siguientes:")
        print("  1. Coloca checkpoint.pth y checkpointMask.pth en este directorio")
        print("  2. Ejecuta este script nuevamente")
        print("  3. O usa: python extract_model_info.py checkpoint.pth\n")
        sys.exit(0)

    # Analizar cada checkpoint
    print("\n" + "="*70)
    print("ANÁLISIS RÁPIDO")
    print("="*70)

    for checkpoint_path in checkpoints:
        analyze_checkpoint(checkpoint_path)

    # Recomendaciones
    print("="*70)
    print("PRÓXIMOS PASOS")
    print("="*70 + "\n")

    print("Para análisis detallado:")
    for checkpoint_path in checkpoints:
        print(f"  python extract_model_info.py {checkpoint_path.name}")

    print("\nPara usar el modelo:")
    print("  1. Revisa GUIA_EXTRACCION_MODELO.md")
    print("  2. Edita load_and_use_model.py con tu arquitectura")
    print("  3. Carga el checkpoint y haz predicciones")

    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    main()
