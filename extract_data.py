#!/usr/bin/env python3
"""
Script provisional para extraer y limpiar dataPumps de Excel a CSV ligero.
Permite especificar ruta de entrada (Excel) y ruta de salida (CSV).
"""
import pandas as pd
import argparse
import os


def extract_to_csv(input_path: str, output_csv: str):
    # 1. Leer Excel con doble encabezado en hoja 'Valores'
    df_raw = pd.read_excel(input_path, sheet_name='Valores', header=[3,4])

    # 2. Aplanar nombres de columnas
    cols = []
    for lvl0, lvl1 in df_raw.columns:
        cols.append(str(lvl1).strip() if pd.notna(lvl1) else str(lvl0).strip())
    df_raw.columns = cols

    # 3. Eliminar primera columna auxiliar (Intervalo)
    if cols:
        df_raw = df_raw.drop(columns=[cols[0]], errors='ignore')

    # 4. Convertir tipos
    df_raw['Fecha'] = pd.to_datetime(df_raw['Fecha'], errors='coerce')
    for col in df_raw.columns:
        if col != 'Fecha':
            df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

    # 5. Guardar CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_raw.to_csv(output_csv, index=False)
    print(f"[✔] CSV limpio guardado en: {output_csv}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extrae dataPumps de Excel a CSV ligero.'
    )
    parser.add_argument(
        '-i', '--input',
        default='data/250312_DataRequest_MetsoPumps.xlsx',
        help='Ruta al archivo Excel fuente (por defecto data/250312_DataRequest_MetsoPumps.xlsx)'
    )
    parser.add_argument(
        '-o', '--output',
        default='data/clean_pumps.csv',
        help='Ruta de salida para el CSV limpio (por defecto data/clean_pumps.csv)'
    )
    args = parser.parse_args()
    extract_to_csv(args.input, args.output)
