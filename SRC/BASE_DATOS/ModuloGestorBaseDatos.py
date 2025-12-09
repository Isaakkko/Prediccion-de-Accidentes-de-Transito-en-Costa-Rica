from GestorBaseDatos import GestorBaseDatos

# Ruta CSV
RUTA_CSV = "c:\GitHubFinal\Prediccion-de-Accidentes-de-Transito-en-Costa-Rica\DATA\PROCESSED\Base_de_accidentes_con_victimas_clean.csv"

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



