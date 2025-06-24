# dashboard.py

"""
Dashboard de operación de bombas
"""
import os
import pandas as pd
import streamlit as st

# 1. Diccionario de agrupación de variables por bomba/línea
VARIABLE_GROUPS = {
    'pump1': [
        'caudalDeAlimentacionNido1M3PerH',
        'presionNido1Psi',
        'ciclonesOperNido1Count',
        'velocidadBomba1Rpm',
        'potenciaBomba1Kw',
        'amperajeBomba1Amp',
        'cwNido1Percent',
        'densidadPulpaNido1Kgxm3',
        'flujoDeAguaDeSelladoBomba1M3PerHr',
        'p80Nido1Um'
    ],
    'pump2': [
        'caudalDeAlimentacionNido2M3PerH',
        'presionNido2Psi',
        'ciclonesOperNido2Count',
        'velocidadBomba2Rpm',
        'potenciaBomba2Kw',
        'amperajeBomba2Amp',
        'cwNido2Percent',
        'densidadPulpaNido2Kgxm3',
        'flujoDeAguaDeSelladoBomba2M3PerHr',
        'p80Nido2Um'
    ],
    'pump3': [
        'caudalDeAlimentacionNido3M3PerH',
        'presionNido3Psi',
        'ciclonesOperNido3Count',
        'velocidadBomba3Rpm',
        'potenciaBomba3Kw',
        'amperajeBomba3Amp',
        'cwNido3Percent',
        'densidadPulpaNido3Kgxm3',
        'flujoDeAguaDeSelladoBomba3M3PerHr',
        'p80Nido3Um'
    ],
    'pump4': [
        'caudalDeAlimentacionNido4M3PerH',
        'presionNido4Psi',
        'ciclonesOperNido4Count',
        'velocidadBomba4Rpm',
        'potenciaBomba4Kw',
        'amperajeBomba4Amp',
        'cwNido4Percent',
        'densidadPulpaNido4Kgxm3',
        'flujoDeAguaDeSelladoBomba4M3PerHr',
        'p80Nido4Um'
    ]
}

@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    """Carga y prepara el DataFrame con índice de fecha"""
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df = df.sort_values('date').set_index('date')
    return df

def main():
    st.set_page_config(page_title="Mill Discharge Dashboard", layout="wide")
    st.title("Mill Discharge Dashboard")

    # Ruta al CSV procesado
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'data', 'processed_pumps.csv')

    # Cargar datos
    df = load_data(csv_path)

    # Selector de bomba
    pump_key = st.sidebar.selectbox(
        "Selecciona bomba/línea",
        list(VARIABLE_GROUPS.keys()),
        index=0
    )
    params = VARIABLE_GROUPS[pump_key]

    # Rango de fechas
    start_date, end_date = st.sidebar.date_input(
        "Rango de fechas", [df.index.min().date(), df.index.max().date()]
    )
    df_sel = df.loc[start_date:end_date, params]

    # Visualización
    st.subheader(f"Parámetros de {pump_key}")
    st.line_chart(df_sel)

if __name__ == "__main__":
    main()
