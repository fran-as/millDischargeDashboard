import os
import pandas as pd
import streamlit as st
import altair as alt

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
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df = df.sort_values('date').set_index('date')
    return df

def main():
    st.set_page_config(page_title="Mill Discharge Dashboard", layout="wide")
    st.title("Mill Discharge Dashboard")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'data', 'processed_pumps.csv')
    df = load_data(csv_path)

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

    # Limpieza de datos numéricos para graficar
    df_plot = df_sel.apply(pd.to_numeric, errors="coerce")
    df_plot = df_plot.loc[:, df_plot.notnull().any()]

    # PRIMER GRÁFICO: Todos los parámetros vs date
    st.subheader(f"Serie temporal de parámetros principales - {pump_key}")
    if not df_plot.empty:
        st.line_chart(df_plot)
    else:
        st.warning("No hay datos numéricos disponibles para graficar en el rango seleccionado.")

    # SEGUNDO GRÁFICO: Scatter presión vs caudal (ahora sí Caudal en X y Presión en Y)
    st.subheader("Scatter: Presión vs Caudal")
    caudal_col = [col for col in params if 'caudal' in col.lower()]
    presion_col = [col for col in params if 'presion' in col.lower()]
    if caudal_col and presion_col:
        scatter_df = df_plot[[caudal_col[0], presion_col[0]]].dropna()
        scatter_df.columns = ['Caudal', 'Presión']
        if not scatter_df.empty:
            chart = alt.Chart(scatter_df).mark_circle(size=60, opacity=0.5).encode(
                x=alt.X('Caudal', title='Caudal (m³/h)'),
                y=alt.Y('Presión', title='Presión (Psi)'),
                tooltip=['Caudal', 'Presión']
            ).properties(
                width=700, height=400
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No hay datos suficientes para graficar presión vs caudal.")
    else:
        st.info("No se encontraron columnas de caudal y presión para la bomba seleccionada.")

if __name__ == "__main__":
    main()
