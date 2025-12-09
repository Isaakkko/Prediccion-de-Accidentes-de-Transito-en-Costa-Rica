from PROCESADOR_EDA_PERSONAS import ProcesadorEDA
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"
RAW_DIR = DATA_DIR / "RAW"
PROCESSED_DIR = DATA_DIR / "PROCESSED"

# ----------------------
# Archivo RAW y archivo limpio
Archivo_raw = RAW_DIR / "3 Base de personas  en accidentes 2018_ 2024_UTF8.csv"
Archivo_limpio = PROCESSED_DIR / "Base_personas_en_accidentes_clean.csv"

print("Usando archivo RAW:", Archivo_raw)
print("Archivo limpio:", Archivo_limpio)

# ----------------------
# Inicializar procesador
procesador = ProcesadorEDA(archivo_crudo=Archivo_raw, archivo_limpio=Archivo_limpio)

# ---------------- EDA ----------------
procesador.exploracion_inicial()

# ---------------- Limpiezas ----------------
procesador.convertir_dia_mes()
procesador.convertir_edad()
procesador.crear_disyuntivas(drop_original=False)

# ---------------- Gráficos ----------------
procesador.personas_por_provincia_y_rol()
procesador.personas_por_edadquinquenal_y_sexo()
procesador.rol_vs_tipo_lesion()
procesador.matriz_correlacion()

# ---------------- Guardar archivo limpio ----------------
procesador.guardar_dataframe(sep=";")
