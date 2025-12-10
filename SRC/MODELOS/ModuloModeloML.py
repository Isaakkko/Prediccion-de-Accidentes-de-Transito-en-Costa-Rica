import pandas as pd
from pathlib import Path
from ClaseModeloML import ModeloML

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "DATA"
PROCESSED_DIR = DATA_DIR / "PROCESSED"

RUTA = PROCESSED_DIR / "Base_de_accidentes_con_victimas_clean.csv"

df = pd.read_csv(RUTA)
df = df.fillna(0)

columnas_x = [
    'Hora_num', 'Dia_num', 'Mes_num',
    'clima_desconocida', 'clima_rural', 'clima_urbana',
    'calzada_desconocida', 'calzada_pendiente', 'calzada_plano',
    'ruta_curva', 'ruta_desconocida', 'ruta_recta'
]

X = df[columnas_x]
y = df['accidente_con muertos o graves']

modelo = ModeloML()
modelo.entrenar(X, y)

nuevo_dato1 = {
    'Hora_num': 22,
    'Dia_num': 5,
    'Mes_num': 3,
    'clima_desconocida': 0,
    'clima_rural': 1,
    'clima_urbana': 0,
    'calzada_desconocida': 0,
    'calzada_pendiente': 0,
    'calzada_plano': 1,
    'ruta_curva': 0,
    'ruta_desconocida': 0,
    'ruta_recta': 1
}

nuevo_dato2 = {
    'Hora_num': 15,
    'Dia_num': 2,
    'Mes_num': 7,
    'clima_desconocida': 0,
    'clima_rural': 0,
    'clima_urbana': 1,
    'calzada_desconocida': 0,
    'calzada_pendiente': 1,
    'calzada_plano': 0,
    'ruta_curva': 1,
    'ruta_desconocida': 0,
    'ruta_recta': 0
}

nuevo_dato3 = {
    'Hora_num': 9,
    'Dia_num': 4,
    'Mes_num': 1,
    'clima_desconocida': 1,
    'clima_rural': 0,
    'clima_urbana': 0,
    'calzada_desconocida': 1,
    'calzada_pendiente': 0,
    'calzada_plano': 0,
    'ruta_curva': 0,
    'ruta_desconocida': 1,
    'ruta_recta': 0
}

resultado1 = modelo.predecir(nuevo_dato1)
resultado2 = modelo.predecir(nuevo_dato2)
resultado3 = modelo.predecir(nuevo_dato3)

print("Predicción dato 1:", resultado1)
print("Predicción dato 2:", resultado2)
print("Predicción dato 3:", resultado3)
