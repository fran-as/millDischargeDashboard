import os
import streamlit as st
import pandas as pd
import altair as alt

# Configuración de la página
st.set_page_config(page_title='Pump Dashboard', layout='wide')

# Rutas de los logos
here = os.path.dirname(__file__)
imgs = os.path.join(here, 'images')
metso_logo = os.path.join(imgs, 'metso_logo.png')
capstone_logo = os.path.join(imgs, 'capstone_logo.png')

# Mostrar logos en la parte superior
top_cols = st.columns([1, 6, 1])
with top_cols[0]:
    st.image(metso_logo, width=120)
with top_cols[2]:
    st.image(capstone_logo, width=120)

# Espacio y título
st.write('')
st.title('📊 Pump Performance Dashboard')

# Definición de secciones con sus columnas asociadas
GROUPS = {
    "CONCENTRADO ROUGHER": [
        "NivelCajonHP003_Percent",
        "VelocidadMotorPU003_Percent",
        "VelocidadPU003_rpm",
        "PotenciaPU003_kW",
    ],
    "ALIMENTACIÓN REMOLIENDA": [
        "NivelCajonHP010_Percent",
        "FlujoDescargaEspumadoPU010_m3xhr",
        "FlujoDescargaPU010_m3xhr2",
        "VelocidadMotorPU010_Percent",
        "VelocidadPU010_rpm",
        "PotenciaPU010_kW",
    ],
    "CONCENTRADO A CLEANER 2": [
        "NivelCajonHP011_Percent",
        "VelocidadMotorPU011_Percent",
        "VelocidadPU011_rpm",
        "PotenciaPU011_kW",
    ],
    "CLEANER SCAVENGER": [
        "NivelCajonHP015_Percent",
        "VelocidadMotorPU015_Percent",
        "VelocidadPU015_rpm",
        "PotenciaPU015_kW",
    ],
    "COLAS CLEANER 2 A CLEANER 1": [
        "NivelCajonHP022_Percent",
        "VelocidadMotorPU022_Percent",
        "VelocidadPU022_rpm",
        "PotenciaPU022_kW",
    ],
    "SISTEMA SPARGING FC-21": [
        "VelocidadPU023_Percent",
        "PotenciaPU023_kW",
    ],
    "SISTEMA SPARGING FC-22": [
        "VelocidadPU024_Percent",
        "PotenciaPU024_kW",
    ],
    "CONCENTRADO SCAVENGER A CLEANER 3": [
        "NivelCajonHP031_Percent",
        "VelocidadMotorPU031_Percent",
        "VelocidadPU031_rpm",
        "PotenciaPU031_kW",
    ],
    "SISTEMA SPARGING FC-31": [
        "VelocidadPU217_Percent",
        "PotenciaPU217_kW",
    ],
    "CONCENTRADO A FILTRO": [
        "NivelTK061_Percent",
        "VelocidadPU061_Percent",
        "VelocidadPU061_rpm",
        "PotenciaPU061_kW",
    ],
    "TK DE FILTRADO": [
        "NivelTK062_Percent",
        "VelocidadPU062_Percent",
        "PotenciaPU062_kW",
    ],
    "DISTRIBUCIÓN DE CAL": [
        "NivelTK242_Percent",
        "VelocidadPU243_Percent",
        "PotenciaPU243_kW",
        "VelocidadPU244_Percent",
        "PotenciaPU244_kW",
    ],
    "ALIMENTACIÓN CICLONES PLANTA DE ARENA": [
        "NivelCajonHP101_Percent",
        "VelocidadMotorPU101_Percent",
        "VelocidadPU101_rpm",
        "FlujoDescargaPU101_m3xhr",
        "Densisdad6415_Kgxm3",
        "PotenciaPU101_kW",
    ],
    "BOMBA 1 U/F ESPESADOR": [
        "NivelTH101_Percent",
        "Densisdad6712_Kgxm3",
        "VelocidadPU200_Percent",
        "PotenciaPU200_kW",
    ],
    "BOMBA 2 U/F ESPESADOR": [
        "NivelTH101_Percent2",
        "VelocidadPU205_Percent",
        "PotenciaPU205_kW",
    ],
    "DISTRIBUCIÓN DE ARENA": [
        "NivelHP102_Percent",
        "Densidad6625_Kgxm3",
        "Densidad6601_Kgxm3",
        "VelocidadMotorPU111_Percent",
        "VelocidadPU111_rpm",
        "PotenciaPU111_kW",
        "VelocidadPU112_Percent",
        "PotenciaPU112_kW",
        "VelocidadPU113_Percent",
        "PotenciaPU113_kW",
    ],
    "DISTRIBUCIÓN DE LAMAS T1": [
        "NivelHP103_Percent",
        "DensidadPU131_Kgxm3",
        "VelocidadPU131_rpm",
        "PotenciaPU131_kW",
    ],
    "U/F ESPESADOR DE RELAVES": [
        "NivelTH002_Percent",
        "FlujoDescargaPU071_m3xhr",
        "DensisdadPU071_Kgxm3",
        "VelocidadMotorPU071_Percent",
        "VelocidadPU071_rpm",
        "PotenciaPU071_kW",
    ],
}

@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    """Carga el CSV limpio con parsing de fechas."""
    return pd.read_csv(csv_path, parse_dates=['Fecha'])

# Función para clasificar tipo de métrica (para colores)
def classify_metric(m: str) -> str:
    if m.startswith('Nivel'): return 'Nivel'
    if m.startswith('VelocidadMotor'): return 'VelocidadMotor'
    if m.endswith('_rpm') or (m.startswith('Velocidad') and 'Motor' not in m): return 'Velocidad'
    if m.startswith('Potencia'): return 'Potencia'
    if m.startswith('FlujoDescargaEspumado'): return 'FlujoEspumado'
    if m.startswith('FlujoDescarga'): return 'Flujo'
    if 'Densidad' in m: return 'Densidad'
    return 'Otros'

# Mapa de colores por tipo
tipo_map = {
    'Nivel': '#1f77b4',
    'VelocidadMotor': '#ff7f0e',
    'Velocidad': '#2ca02c',
    'Potencia': '#d62728',
    'FlujoEspumado': '#9467bd',
    'Flujo': '#8c564b',
    'Densidad': '#e377c2',
    'Otros': '#7f7f7f'
}

# Sidebar: ruta al CSV y selección de sección
data_path = st.sidebar.text_input('Ruta al CSV limpio', 'data/clean_pumps.csv')
section = st.sidebar.selectbox('Selecciona sección', list(GROUPS.keys()))

# Carga y filtrado de los datos
df = load_data(data_path)
cols = GROUPS[section]
df_section = df[['Fecha'] + cols]

# Transformación a formato largo e inclusión de columna 'tipo'
df_long = (
    df_section
    .melt(id_vars='Fecha', var_name='metric', value_name='valor')
    .assign(tipo=lambda d: d['metric'].apply(classify_metric))
)

# ===== Gráficos y tablas =====
# 1) Series de tiempo
present_types = df_long['tipo'].unique().tolist()
palette = [tipo_map[t] for t in present_types]

chart = alt.Chart(df_long).mark_line().encode(
    x='Fecha:T',
    y='valor:Q',
    color=alt.Color('tipo:N', scale=alt.Scale(domain=present_types, range=palette), legend=alt.Legend(title='Tipo')),
    tooltip=['Fecha:T', 'metric:N', 'valor:Q']
).interactive().properties(width='container', height=350)
st.altair_chart(chart, use_container_width=True)

# 2) Estadísticas descriptivas
st.header('Estadísticas descriptivas')
st.dataframe(
    df_long
    .groupby(['tipo', 'metric'])['valor']
    .agg(['count','mean','min','max','std'])
    .reset_index()
)

# 3) Relaciones de flujo
st.header('Relaciones de flujo')
flows = [c for c in cols if 'Flujo' in c]
pows = [c for c in cols if 'Potencia' in c]
levels = [c for c in cols if 'Nivel' in c]
if flows and pows:
    for f in flows:
        for p in pows:
            st.subheader(f'{f} vs {p}')
            scatter = alt.Chart(df_section).mark_circle(size=60).encode(
                x=alt.X(f+':Q', title=f),
                y=alt.Y(p+':Q', title=p),
                color=alt.value(tipo_map['Potencia']),
                tooltip=['Fecha:T', f+':Q', p+':Q']
            ).interactive().properties(width='container', height=300)
            st.altair_chart(scatter, use_container_width=True)
if flows and levels:
    for f in flows:
        for l in levels:
            st.subheader(f'{f} vs {l}')
            scatter = alt.Chart(df_section).mark_circle(size=60).encode(
                x=alt.X(f+':Q', title=f),
                y=alt.Y(l+':Q', title=l),
                color=alt.value(tipo_map['Velocidad']),
                tooltip=['Fecha:T', f+':Q', l+':Q']
            ).interactive().properties(width='container', height=300)
            st.altair_chart(scatter, use_container_width=True)

# 4) Box-and-Whisker por métrica
st.header('Distribución de métricas')
df = df_long
metrics = cols
cols_streamlit = st.columns(3)
for idx, metric in enumerate(metrics):
    data = df[df['metric'] == metric]
    box = alt.Chart(data).mark_boxplot(size=60, extent='min-max').encode(
        y=alt.Y('valor:Q', title='Valor'),
        color=alt.value(tipo_map[classify_metric(metric)])
    )
    df_mean = pd.DataFrame({'media': [data['valor'].mean()]})
    mean = alt.Chart(df_mean).mark_point(shape='diamond', size=120, color='black').encode(
        y='media:Q'
    )
    chart = alt.layer(box, mean).properties(
        title=metric, width=250, height=350
    )
    col = cols_streamlit[idx % 3]
    with col:
        st.altair_chart(chart, use_container_width=True)

st.markdown('---')
st.write('✌️ Fin del análisis')
