import pandas as pd
from ClaseModeloML import ModeloML

#  Cargar datos
df = pd.read_csv(r"C:\GitFinaall\Prediccion-de-Accidentes-de-Transito-en-Costa-Rica\DATA\PROCESSED\Base_de_accidentes_con_victimas_clean.csv")
df = df.fillna(0)

#  Variables de entrada
columnas_x = [
    'Hora_num', 'Dia_num', 'Mes_num',
    'clima_desconocida', 'clima_rural', 'clima_urbana',
    'calzada_desconocida', 'calzada_pendiente', 'calzada_plano',
    'ruta_curva', 'ruta_desconocida', 'ruta_recta'
]

X = df[columnas_x]

# Variable objetivo
y = df['accidente_con muertos o graves']

# Crear modelo
modelo = ModeloML()

# Entrenar 
modelo.entrenar(X, y)

# Probar con un nuevos datos
nuevo_dato1 = {
    'Hora_num': 22,     # Se especifica la hora 
    'Dia_num': 5,       # Se pone el numero del dia 
    'Mes_num': 3,       # Se pone numero del mes 
    'clima_desconocida': 0, # Clima 0 porque no es desconocido
    'clima_rural': 1,   # Clima rural 1 porque el accidente ocurrio en una zona rural 
    'clima_urbana': 0,  # Clima urbano 0 porque no ocurrio en zona urbana
    'calzada_desconocida': 0,   # Calzada 0 porque no es desconocido
    'calzada_pendiente': 0,     # Calzada pendiente 0 porque no es desconocido 
    'calzada_plano': 1,    # calzada plana 1 porque ocurrio en calzada plana
    'ruta_curva': 0,       # Ruta curva 0 porque no tiene curva 
    'ruta_desconocida': 0, # Ruta desconocida 0 porque no es desconocida 
    'ruta_recta': 1     # Ruta recta 1 porque la ruta si fue recta
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


print("Predicción del nuevo dato:", resultado1)
print("Predicción del nuevo dato:", resultado2)
print("Predicción del nuevo dato:", resultado3)




