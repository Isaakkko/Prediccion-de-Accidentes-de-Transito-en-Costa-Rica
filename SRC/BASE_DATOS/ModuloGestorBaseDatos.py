from pathlib import Path
from GestorBaseDatos import GestorBaseDatos

# -----------------------
# Rutas del proyecto

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "DATA"
PROCESSED_DIR = DATA_DIR / "PROCESSED"

# Ruta CSV (PROCESSED)
RUTA_CSV = PROCESSED_DIR / "Base_de_accidentes_con_victimas_clean.csv"

print("Usando CSV:", RUTA_CSV)
print("Existe archivo?:", RUTA_CSV.exists())

# Crear gestor base datos
db = GestorBaseDatos("accidentes.db")

# Crear tabla accidentes
df = db.crear_tabla_desde_csv("accidentes", RUTA_CSV)

print("Base de datos creada y tabla 'accidentes' poblada correctamente.")
print(df.head())

# Consulta de accidentes con muertos o graves
resultado = db.ejecutar_consulta("""
    SELECT *
    FROM accidentes
    WHERE `accidente_con muertos o graves` = 1
""")
print(resultado)

# Consulta de accidentes por provincia
resultado = db.ejecutar_consulta("""
    SELECT Provincia, COUNT(*) AS total_accidentes
    FROM accidentes
    GROUP BY Provincia
""")
print(resultado)

# Accidentes por estado del tiempo
resultado = db.ejecutar_consulta("""
    SELECT `Estado del tiempo`,
           COUNT(*) AS total_accidentes
    FROM accidentes
    GROUP BY `Estado del tiempo`
    ORDER BY total_accidentes DESC
""")
print(resultado)
