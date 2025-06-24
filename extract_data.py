#!/usr/bin/env python
"""
extract_data.py

Este script carga el archivo de datos en Excel, normaliza los nombres de columna a camelCase,
convierte la columna "date" a datetime y exporta un CSV optimizado para el dashboard.
Además, limpia cualquier valor no numérico o nulo, asegurando compatibilidad para análisis.
"""
import os
import numpy as np
import pandas as pd

# Mapeo de sufijos a notación camelCase (ajusta según tus convenciones)
_SUFFIX_MAP = {
    'm3xh': 'M3PerH',
    'm3xhr': 'M3PerHr',
    'psi': 'Psi',
    'cant': 'Count',
    'rpm': 'Rpm',
    'kw': 'Kw',
    'amp': 'Amp',
    'prctj': 'Percent',
    'kgperm3': 'KgPerM3',
    'kgxm3': 'Kgxm3',
    'um': 'Um',
}

def _normalize_columns(columns):
    """Normaliza una lista de nombres de columna a lowerCamelCase."""
    new_cols = []
    for col in columns:
        name = str(col).strip()
        if name.lower() == 'date':
            new_cols.append('date')
            continue
        parts = name.split('_')
        if len(parts) > 1:
            base = ''.join(parts[:-1])
            suffix = parts[-1].lower()
            suffix_norm = _SUFFIX_MAP.get(suffix, suffix.capitalize())
            raw = base + suffix_norm
        else:
            raw = parts[0]
        # Garantizar lowerCamelCase
        normalized = raw[0].lower() + raw[1:]
        new_cols.append(normalized)
    return new_cols

def extract(input_path: str, output_path: str):
    # Cargar datos
    df = pd.read_excel(input_path)
    print(f"[INFO] Datos cargados: {df.shape[0]} filas x {df.shape[1]} columnas")

    # Normalizar columnas
    df.columns = _normalize_columns(df.columns)
    print(f"[INFO] Columnas normalizadas: {df.columns.tolist()}")

    # Convertir "date" a datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Limpieza: Forzar a numérico (salvo la fecha)
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # (Opcional) Reemplazar valores típicos de null por NaN
    df.replace(['NULL', '', 'nan', 'NaN', 'None', None], np.nan, inplace=True)

    # Resumen rápido de faltantes
    missing = df.isna().sum()
    print("[INFO] Valores faltantes por columna:")
    print(missing[missing > 0])

    # Guardar CSV optimizado
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] CSV procesado guardado en: {output_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'data', 'dataPumps.xlsx')
    output_file = os.path.join(base_dir, 'data', 'processed_pumps.csv')
    extract(input_file, output_file)
