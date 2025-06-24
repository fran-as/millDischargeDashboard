#!/usr/bin/env bash

# Activa entorno virtual
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  echo "Entorno virtual no encontrado. Crea uno con: python3 -m venv .venv"
  exit 1
fi

# Ejecuta el ETL para procesar datos
echo "[*] Ejecutando extract_data.py..."
python extract_data.py
if [ $? -ne 0 ]; then
  echo "[!] Error al procesar datos. Revisa extract_data.py"
  exit 1
fi

# Arranca el dashboard en modo local
echo "[*] Iniciando Streamlit..."
streamlit run dashboard.py
