from PROCESADOR_EDA import ProcesadorEDA
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"
RAW_DIR = DATA_DIR / "RAW"
PROCESSED_DIR = DATA_DIR / "PROCESSED"

# ----------------------
# archivo raw VICTIMAS
Archivo_raw = RAW_DIR / "2 Base de accidentes con victimas 2018_ 2024_UTF8.csv"
Archivo_limpio = PROCESSED_DIR / "Base_de_accidentes_con_victimas_clean.csv"

print("Usando archivo RAW:", Archivo_raw)  # debug opcional, para que veas la ruta real

procesador = ProcesadorEDA(archivo_crudo=Archivo_raw, archivo_limpio=Archivo_limpio)
#----------------
procesador.exploracion_inicial()
procesador.convertir_dia_mes()
procesador.crear_disyuntivas()
procesador.frecuencia_provincia_hora()
procesador.mapa_calor_zona()
procesador.accidente_vs_clima()
procesador.matriz_correlacion()
#--------------
procesador.guardar_dataframe()

