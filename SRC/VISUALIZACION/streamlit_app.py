import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
import plotly.express as px
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ==============================
# Configurar la página
# ==============================
st.set_page_config(page_title="Análisis de Personas en Accidentes", layout="wide")

# Título principal
st.title("📊 Análisis de Personas en Accidentes de Tránsito")

# -----------------------------
# Construir ruta absoluta
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "DATA"
PROCESSED_DIR = DATA_DIR / "PROCESSED"

RUTA = PROCESSED_DIR / "Base_personas_en_accidentes_clean.csv"


# -----------------------------
# Cargar datos
# -----------------------------
@st.cache_data
def cargar_datos():
    df_local = pd.read_csv(RUTA, sep=';')
    df_local.columns = df_local.columns.str.strip()
    return df_local


df = cargar_datos()
st.sidebar.success(f"✅ Datos cargados: {len(df):,} registros")

# ==============================
# Sidebar: info + filtros
# ==============================
st.sidebar.header("Opciones")

mostrar_info = st.sidebar.checkbox("Mostrar información del dataset")

if mostrar_info:
    st.subheader("Información del Dataset")
    st.write(f"Total de registros: {len(df):,}")
    st.write(f"Columnas: {len(df.columns)}")
    st.dataframe(df.head())

# Selector de año
if "Año" in df.columns:
    año_seleccionado = st.sidebar.selectbox(
        "Seleccionar año",
        sorted(df["Año"].dropna().unique())
    )
    df_base = df[df["Año"] == año_seleccionado]
else:
    año_seleccionado = None
    df_base = df

# Filtro de provincias (sobre los datos ya filtrados por año)
if "Provincia" in df_base.columns:
    provincias_disp = sorted(df_base["Provincia"].dropna().unique())
    provincias_sel = st.sidebar.multiselect(
        "Provincia",
        provincias_disp,
        default=provincias_disp
    )
else:
    provincias_sel = None

# Filtro de tipo de accidente (si existe la columna)
if "Tipo de accidente" in df_base.columns:
    tipos_disp = sorted(df_base["Tipo de accidente"].dropna().unique())
    tipos_sel = st.sidebar.multiselect(
        "Tipo de accidente",
        tipos_disp,
        default=tipos_disp
    )
else:
    tipos_sel = None

# Aplicar filtros (si existen)
df_f = df_base.copy()

if provincias_sel is not None:
    df_f = df_f[df_f["Provincia"].isin(provincias_sel)]

if tipos_sel is not None:
    df_f = df_f[df_f["Tipo de accidente"].isin(tipos_sel)]

# Coordenadas aproximadas por provincia (centroides)
coords_provincias = {
    "san josé": {"lat": 9.9281, "lon": -84.0907},
    "alajuela": {"lat": 10.0163, "lon": -84.2116},
    "cartago": {"lat": 9.8644, "lon": -83.9194},
    "heredia": {"lat": 9.9970, "lon": -84.1160},
    "guanacaste": {"lat": 10.6350, "lon": -85.4377},
    "puntarenas": {"lat": 9.9763, "lon": -84.8389},
    "limón": {"lat": 9.9907, "lon": -83.0350}
}

# =====================================================
# 1. Personas por Provincia y Rol  (SIN filtros, dataset completo)
# =====================================================
st.header("1. Frecuencia por Provincia y Rol")
if "Provincia" in df.columns and "Rol" in df.columns:
    tabla = df.groupby(["Provincia", "Rol"]).size().reset_index(name="conteo")
    pivot = tabla.pivot(index="Provincia", columns="Rol", values="conteo").fillna(0)

    fig1, ax1 = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot, cmap="viridis", annot=True, fmt='.0f', ax=ax1)
    ax1.set_title("Frecuencia por provincia y rol", fontsize=16, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig1)
else:
    st.error("Las columnas 'Provincia' o 'Rol' no se encontraron en el dataset")

# =====================================================
# 2. Personas por Grupo de Edad y Sexo (SIN filtros)
# =====================================================
st.header("2. Personas por Grupo de Edad y Sexo")
if "Edad quinquenal" in df.columns and "Sexo" in df.columns:
    tabla = df.groupby(["Edad quinquenal", "Sexo"]).size().reset_index(name="conteo")
    pivot = tabla.pivot(index="Edad quinquenal", columns="Sexo", values="conteo").fillna(0)

    fig2, ax2 = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, cmap="magma", annot=True, fmt='.0f', ax=ax2)
    ax2.set_title("Personas por grupo de edad y sexo", fontsize=16, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig2)
else:
    st.error("Las columnas 'Edad quinquenal' o 'Sexo' no se encontraron en el dataset")

# =====================================================
# 3. Rol vs Tipo de Lesión (SIN filtros)
# =====================================================
st.header("3. Rol vs Tipo de Lesión")
if "Rol" in df.columns and "Tipo de lesión" in df.columns:
    tabla = df.groupby(["Rol", "Tipo de lesión"]).size().reset_index(name="conteo")
    pivot = tabla.pivot(index="Rol", columns="Tipo de lesión", values="conteo").fillna(0)

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, cmap="coolwarm", annot=True, fmt='.0f', ax=ax3)
    ax3.set_title("Rol vs tipo de lesión", fontsize=16, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig3)
else:
    st.error("Las columnas 'Rol' o 'Tipo de lesión' no se encontraron en el dataset")

# =====================================================
# 4. Barras + Mapa geográfico por provincia (FILTROS APLICADOS)
# =====================================================
st.header("4. Accidentes por provincia (barras + mapa)")

if "Provincia" in df_f.columns:

    # ---------- Barras por provincia ----------
    df_prov = df_f.groupby("Provincia").size().reset_index(name="Total")

    fig_barras = px.bar(
        df_prov,
        x="Provincia",
        y="Total",
        title="Total de accidentes/personas por provincia (datos filtrados)",
        text="Total"
    )
    fig_barras.update_traces(textposition="outside")
    st.plotly_chart(fig_barras, use_container_width=True)

    # ---------- Mapa Folium por provincia ----------
    st.subheader("Mapa de accidentes por provincia")

    m = folium.Map(location=[9.93, -84.08], zoom_start=8)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_prov.iterrows():
        prov = str(row["Provincia"]).strip().lower()
        total = int(row["Total"])

        if prov in coords_provincias:
            lat = coords_provincias[prov]["lat"]
            lon = coords_provincias[prov]["lon"]

            folium.Marker(
                location=[lat, lon],
                popup=f"Provincia: {prov.title()}<br>Total: {total}",
                tooltip=f"{prov.title()} – {total}"
            ).add_to(marker_cluster)

    st_folium(m, width=900, height=500)

else:
    st.error("La columna 'Provincia' no se encuentra en el dataset")

# =====================================================
# 5. Mapa geográfico por cantón (FILTROS APLICADOS)
# =====================================================
st.header("5. Mapa geográfico de accidentes por cantón")

if {"Cantón", "Provincia"}.issubset(df_f.columns):

    df_cant = (
        df_f
        .groupby(["Provincia", "Cantón"])
        .size()
        .reset_index(name="conteo")
    )

    df_cant["prov_norm"] = df_cant["Provincia"].str.strip().str.lower()
    df_cant["lat"] = np.nan
    df_cant["lon"] = np.nan

    for prov_norm, sub in df_cant.groupby("prov_norm"):
        base = coords_provincias.get(prov_norm)
        if base is None:
            continue

        n = len(sub)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        radius = 0.3

        df_cant.loc[sub.index, "lat"] = base["lat"] + radius * np.cos(angles)
        df_cant.loc[sub.index, "lon"] = base["lon"] + radius * np.sin(angles)

    df_cant_mapa = df_cant.dropna(subset=["lat", "lon"])

    if df_cant_mapa.empty:
        st.warning("No hay datos para este año/filtros o no se pudieron ubicar los cantones.")
    else:
        fig_cant = px.scatter_mapbox(
            df_cant_mapa,
            lat="lat",
            lon="lon",
            size="conteo",
            color="Provincia",
            hover_name="Cantón",
            hover_data={"Provincia": True, "conteo": True, "lat": False, "lon": False},
            size_max=25,
            zoom=7,
            title="Accidentes por cantón (datos filtrados)",
        )

        fig_cant.update_layout(
            mapbox_style="open-street-map",
            margin=dict(r=0, l=0, t=40, b=0)
        )

        st.plotly_chart(fig_cant, use_container_width=True)
else:
    st.error("Las columnas 'Cantón' y/o 'Provincia' no se encuentran en el dataset")

# ==============================
# Footer
# ==============================
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📌 Instrucciones
1. Asegúrate de tener el CSV en `DATA/PROCESSED`.
2. Desde la raíz del proyecto ejecuta:

   `python -m streamlit run SRC/VISUALIZACION/streamlit_app.py`

3. Usa los filtros del panel izquierdo para explorar los datos.
""")
#cd "C:\Users\isaac\Documents\Prediccion-de-Accidentes-de-Transito-en-Costa-Rica"
#python -m streamlit run SRC/VISUALIZACION/streamlit_app.py