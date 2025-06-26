#!/usr/bin/env python
"""
extract_data.py

Carga el archivo Excel, normaliza columnas, limpia valores y exporta el CSV
redondeando todos los valores numéricos a 3 decimales.
"""
import os
import numpy as np
import pandas as pd

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
        normalized = raw[0].lower() + raw[1:]
        new_cols.append(normalized)
    return new_cols

def extract(input_path: str, output_path: str):
    df = pd.read_excel(input_path)
    print(f"[INFO] Datos cargados: {df.shape[0]} filas x {df.shape[1]} columnas")
    df.columns = _normalize_columns(df.columns)
    print(f"[INFO] Columnas normalizadas: {df.columns.tolist()}")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df.replace(['NULL', '', 'nan', 'NaN', 'None', None], np.nan, inplace=True)
    # Redondear todo lo numérico a 3 decimales
    for col in df.columns:
        if col != 'date' and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].round(3)
    missing = df.isna().sum()
    print("[INFO] Valores faltantes por columna:")
    print(missing[missing > 0])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] CSV procesado guardado en: {output_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'data', 'dataPumps.xlsx')
    output_file = os.path.join(base_dir, 'data', 'processed_pumps.csv')
    extract(input_file, output_file)
