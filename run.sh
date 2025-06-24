#!/usr/bin/env bash
set -euo pipefail

env_dir=".venv"

# 1. Crear virtualenv si falta
if [ ! -d "$env_dir" ]; then
  echo "[INFO] Creando entorno virtual en $env_dir..."
  python3 -m venv "$env_dir"
fi

# 2. Activar virtualenv
echo "[INFO] Activando entorno virtual..."
# shellcheck disable=SC1091
source "$env_dir/bin/activate"

# 3. Actualizar pip e instalar requisitos
echo "[INFO] Actualizando pip e instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Extraer y limpiar a CSV
echo "[INFO] Extrayendo CSV limpio desde el Excel..."
python extract_data.py \
  --input data/250312_DataRequest_MetsoPumps.xlsx \
  --output data/clean_pumps.csv

# 5. Ejecutar Streamlit
echo "[INFO] Iniciando Streamlit dashboard..."
streamlit run dashboard.py
