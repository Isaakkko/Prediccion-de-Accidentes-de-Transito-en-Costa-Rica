import pandas as pd
from pathlib import Path

class cargador_datos:


    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.data = None
        self.filas = 0
        self.columnas = 0
        self.porcentaje_nulos = 0
        self.duplicados = 0

    def cargar_datos(self):
        # Leer el archivo CSV
        self.data = pd.read_csv(self.ruta_csv)

        # Obtener dimensiones del dataset
        self.filas, self.columnas = self.data.shape

        # Calcular porcentaje de nulos
        total_celdas = self.filas * self.filas
        total_celdas = self.filas * self.columnas
        total_nulos = self.data.isnull().sum().sum()
        self.porcentaje_nulos = (total_nulos / total_celdas) * 100

        # Calcular registros duplicados
        self.duplicados = self.data.duplicated().sum()

    def resumen(self):
        print("Filas:", self.filas)
        print("Columnas:", self.columnas)
        print("Porcentaje de nulos:", round(self.porcentaje_nulos, 2), "%")
        print("Duplicados:", self.duplicados)



BASE_DIR = Path(__file__).resolve().parent

accidentes_victimas = BASE_DIR / "RAW" / "2 Base de accidentes con victimas 2018_ 2024_UTF8.csv"
personas_accidentes = BASE_DIR / "RAW" / "3 Base de personas  en accidentes 2018_ 2024_UTF8.csv"

print("\nBase de accidentes con victimas")
cargador = cargador_datos(accidentes_victimas)
cargador.cargar_datos()
cargador.resumen()

print("\npersonas  en accidentes")
cargador2 = cargador_datos(personas_accidentes)
cargador2.cargar_datos()
cargador2.resumen()