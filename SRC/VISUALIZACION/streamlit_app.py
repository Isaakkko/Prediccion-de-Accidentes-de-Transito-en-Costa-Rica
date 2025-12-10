import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# Configurar la página
st.set_page_config(page_title="Análisis de Personas en Accidentes", layout="wide")

# Título principal
st.title("📊 Análisis de Personas en Accidentes de Tránsito")

# -----------------------------
# Construir ruta absoluta
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "DATA"
PROCESSED_DIR = DATA_DIR / "PROCESSED"

RUTA = PROCESSED_DIR / "Base_personas_en_accidentes_clean.csv"

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv(RUTA, sep=';')

df = cargar_datos()
st.sidebar.success(f"✅ Datos cargados: {len(df):,} registros")

# Sidebar con opciones
st.sidebar.header("Opciones")
mostrar_info = st.sidebar.checkbox("Mostrar información del dataset")

if mostrar_info:
    st.subheader("Información del Dataset")
    st.write(f"Total de registros: {len(df):,}")
    st.write(f"Columnas: {len(df.columns)}")
    st.dataframe(df.head())

# Gráfico 1: Personas por Provincia y Rol
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

# Gráfico 2: Personas por Edad Quinquenal y Sexo
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

# Gráfico 3: Rol vs Tipo de Lesión
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

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Instrucciones")
st.sidebar.markdown("""
1. Asegúrate de tener el CSV en la misma carpeta
2. Ejecuta: `streamlit run streamlit_app.py`
3. Los gráficos se actualizarán automáticamente
""")

#cd C:\Users\isaac\Documents\Prediccion-de-Accidentes-de-Transito-en-Costa-Rica
#streamlit run SRC/VISUALIZACION/streamlit_app.py
