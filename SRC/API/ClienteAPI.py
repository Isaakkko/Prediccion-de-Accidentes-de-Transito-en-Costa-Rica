import requests             # Librerias necesarias
import pandas as pd          # vistas en clase

class ClienteAPI:
    def __init__(self, api_key):
        self.api_key = api_key   # API KEY >>> "dc8e7025067eecf8b375796b2d87deb7"               
        self.url = "https://api.openweathermap.org/data/2.5/weather"    # url de la API

    def clima_ciudad(self, ciudad):
        params = {
            "q": ciudad,        # Nombre de la ciudad a consultar
            "appid": self.api_key,  # se usa el API key para que se complete la consulta  
            "units": "metric"   # Devuelve la temperatura en celsius (originalmente la da en kelvin)
        }

        respuesta = requests.get(self.url, params=params)  # Llama al API usando la url y parametros 
        data = respuesta.json()   # Convierte la respuesta JSON de la API en un diccionario python

        clima = {                      # Se extrae la informacion util 
            "Ciudad": data['name'],     # Nombre de la ciudad
            "Temperatura (°C)": data['main']['temp'],   # Grados celsius actuales
            "Sensación Térmica (°C)": data['main']['feels_like'],  # Como se siente la temperatura 
            "Humedad (%)": data['main']['humidity'],    # Porcentaje de humedad 
            "Presión (hPa)": data['main']['pressure'],   # Presion atmosferica
            "Velocidad del Viento (m/s)": data['wind']['speed'],   # Velocidad del viento 
            "País": data['sys']['country']  # Pais al que pertenece la ciudad 
        }

        return pd.DataFrame([clima])    # Convertimos el diccionario en un solo dataframe



