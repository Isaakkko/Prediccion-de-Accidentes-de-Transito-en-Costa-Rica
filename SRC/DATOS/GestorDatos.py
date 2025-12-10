import pandas as pd
from pathlib import Path


class CargadorDatos:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.data = None
        self.filas = 0
        self.columnas = 0
        self.porcentaje_nulos = 0
        self.duplicados = 0

    def cargar_datos(self):
        # Leer el archivo CSV
        print("Leyendo archivo:", self.ruta_csv)
        print("Existe?:", self.ruta_csv.exists())
        self.data = pd.read_csv(self.ruta_csv)   # si son ; pon sep=";"

        # Dimensiones del dataset
        self.filas, self.columnas = self.data.shape

        # Calcular porcentaje de nulos
        total_celdas = self.filas * self.columnas     # aquí tenías filas*filas primero
        total_nulos = self.data.isnull().sum().sum()
        self.porcentaje_nulos = (total_nulos / total_celdas) * 100

        # Registros duplicados
        self.duplicados = self.data.duplicated().sum()

    def resumen(self):
        print("Filas:", self.filas)
        print("Columnas:", self.columnas)
        print("Porcentaje de nulos:", round(self.porcentaje_nulos, 2), "%")
        print("Duplicados:", self.duplicados)


# ================== RUTAS DEL PROYECTO ==================

# ...\Prediccion-de-Accidentes-de-Transito-en-Costa-Rica
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"
RAW_DIR = DATA_DIR / "RAW"

accidentes_victimas = RAW_DIR / "2 Base de accidentes con victimas 2018_ 2024_UTF8.csv"
personas_accidentes = RAW_DIR / "3 Base de personas  en accidentes 2018_ 2024_UTF8.csv"

# ================== USO DEL CARGADOR ==================

print("\nBase de accidentes con victimas")
cargador = CargadorDatos(accidentes_victimas)
cargador.cargar_datos()
cargador.resumen()

print("\nPersonas en accidentes")
cargador2 = CargadorDatos(personas_accidentes)
cargador2.cargar_datos()
cargador2.resumen()

# Juntar los CSV
df_accidentes_victimas_personas_accidentes = pd.concat(
    [cargador.data, cargador2.data],
    ignore_index=True
)

print("\nDataFrame combinado:")
print(df_accidentes_victimas_personas_accidentes.head())
print("Filas totales:", df_accidentes_victimas_personas_accidentes.shape[0])
print("Columnas totales:", df_accidentes_victimas_personas_accidentes.shape[1])

# Guardar archivo combinado
salida = RAW_DIR / "df_accidentes_victimas_&_personas_accidentes_2018_2024.csv"
df_accidentes_victimas_personas_accidentes.to_csv(salida, index=False, encoding="utf-8")
print("\nCSV combinado guardado en:", salida)
