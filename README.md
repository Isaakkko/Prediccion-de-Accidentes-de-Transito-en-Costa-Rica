# 🚦 Predicción de Accidentes de Tránsito en Costa Rica  
**Proyecto 4 – Análisis y Modelo Predictivo**  
**Colegio Universitario de Cartago – Costa Rica**

**Integrantes:**  
- Isaac Ulloa Calvo  
- Jeffrey Jiménez Cordero  
- Felipe Montenegro Artavia  

---

## 📌 Descripción General  
Este proyecto desarrolla un sistema de análisis y predicción de accidentes de tránsito en Costa Rica.  
Incluye:

- Análisis exploratorio de datos (EDA)  
- Visualizaciones por provincias, zonas y condiciones climáticas  
- Integración de datos externos (API climática)  
- Modelos supervisados de clasificación para predecir la ocurrencia de accidentes  

El objetivo es identificar los factores que influyen en los accidentes de tránsito y construir un modelo capaz de estimar la probabilidad de ocurrencia según la provincia, condiciones del clima y variables temporales.

---

## 📁 Fuentes de Datos

### 🗂 1. Dataset principal — COSEVI  
Datos históricos de accidentes en Costa Rica:  
🔗 https://www.csv.go.cr/estad%C3%ADsticas

Incluye información como:  
- Provincia y cantón  
- Tipo de accidente  
- Fecha y hora  
- Condiciones de la vía  
- Número de víctimas  

---

### 🌧 2. API Climática — Open-Meteo Archive  
Se utiliza para agregar variables meteorológicas al dataset:  
🔗 https://archive-api.open-meteo.com/v1/archive?latitude=9.93&longitude=-84.08&start_date=2023-01-01&end_date=2023-12-31&daily=precipitation_sum&timezone=America%2FCosta_Rica

Variables obtenidas:
- Lluvia acumulada diaria  
- Otras variables dependiendo del endpoint  

---

### 🗄 3. Base de Datos Local  
El proyecto contempla almacenar los datos limpios en SQLite o SQL Server para consultas agregadas y análisis más estructurado.

---

## 🧪 Análisis Exploratorio y Visualización (EDA)

El análisis incluye:

### ✔ Distribución y frecuencia  
- Accidentes por provincia  
- Accidentes por hora del día  
- Accidentes por día de la semana  

### ✔ Correlaciones y mapas de calor  
- Variables de clima vs accidentes  
- Provincia vs tipo de accidente  

### ✔ Resultados clave  
- Identificación de zonas críticas  
- Comparación entre accidentes en días lluviosos y secos  
- Impacto del tipo de vía  

---

## 🤖 Modelo Predictivo

### 🎯 Tipo de problema  
**Clasificación binaria** — Predecir si ocurrirá un accidente (Sí/No).

### 🔢 Algoritmos utilizados  
- K-Nearest Neighbors (KNN)

### 🧩 Variables de entrada  
- Hora del día  
- Día de la semana  
- Provincia  
- Mes del año
- Clima
- Tipo de calzada
- Tipo de ruta

### 🎯 Variable objetivo  
- **Accidente** (1 = Sí, 0 = No)

## 🧱 Arquitectura del Proyecto
```
Prediccion-de-Accidentes-de-Transito-en-Costa-Rica/
│
├── SRC/
│   ├── DATOS/
│   │   └── GestorDatos
│   │
│   ├── BASE_DATOS/
│   │   ├── GestorBaseDatos
│   │   └── ModuloGestorBaseDatos
│   │
│   ├── API/
│   │   ├── ClienteAPI
│   │   └── ModuloClienteAPI
│   │
│   ├── EDA/
│   │   ├── modulo
│   │   ├── modulo_personas
│   │   ├── PROCESADOR_EDA
│   │   └── PROCESADOR_EDA_PERSONAS
│   │
│   ├── VISUALIZACION/
│   │   └── Visualizacion_accidentes
│   │
│   ├── MODELOS/
│   │   ├── ClaseModeloML
│   │   └── ModuloModeloML
│   │
│   └── HELPERS/
│       └── UTILIDADES
│
├── MAIN.py
│
├── NOTEBOOKS/
│   └── EXPLORACION_INICIAL.ipynb
│
└── DATA/
    ├── PROCESSED/
    │   ├── Base_personas_en_accidentes_clean.csv
    │   └── Base_de_accidentes_con_victimas_clean.csv
    │
    └── RAW/
        ├── 2 Base de accidentes con victimas 2018_2024_UTF8.csv
        └── 3 Base de personas en accidentes 2018_2024_UTF8.csv
```
 ## ⚙️ Requerimientos Técnicos

### 🐍 Python 3.10+  
### 📚 Librerías:
- pandas  
- numpy  
- matplotlib  
- seaborn  
- scikit-learn  
- requests  
- sqlite3 / pyodbc  }

## 📈 Resultados Esperados

Relación entre lluvia y número de accidentes

Identificación de provincias con mayor incidencia

Horarios y días más peligrosos

Predicción de ocurrencia de accidentes mediante ML

Métricas del desempeño del modelo

## 🧾 Conclusiones

La lluvia aumenta la probabilidad de accidentes, especialmente en zonas con alta densidad vehicular.

Las provincias con mayor concentración urbana poseen más casos reportados.

Los modelos supervisados ofrecen una predicción útil para análisis preventivos.

La combinación de datos de COSEVI con API climática mejora significativamente el análisis.

# Fin
