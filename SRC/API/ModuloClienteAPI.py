from ClienteAPI import ClienteAPI

API_KEY = "dc8e7025067eecf8b375796b2d87deb7"

cliente = ClienteAPI(API_KEY)

df = cliente.clima_ciudad("Cartago, CR")

print(df)
