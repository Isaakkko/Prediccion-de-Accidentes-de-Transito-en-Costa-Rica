#Importacion de librerias necesarias para los graficos
import pandas as pd
import matplotlib.pyplot as plt

#Creacion de la clase visualizador

class Visualizador:
    def __init__(self, datos):
        if isinstance(datos, str):
            self.df = pd.read_csv(datos)
        elif isinstance(datos, pd.DataFrame):
            self.df = datos
        else:
            raise TypeError("Debe ser una ruta de archivo o un DataFrame")
        print(f"Datos cargados: {len(self.df)} registros")
    

    #Grafico de la cantidad total de accidentes por provincia
    def grafico_accidentes_por_provincia(self):
        accidentes_provincia = self.df['Provincia'].value_counts()
        plt.figure(figsize=(12, 6))
        plt.bar(accidentes_provincia.index, accidentes_provincia.values, color='steelblue')
        plt.title('Cantidad de Accidentes por Provincia', fontsize=16, fontweight='bold')
        plt.xlabel('Provincia', fontsize=12)
        plt.ylabel('Cantidad de Accidentes', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()


    #Grafico sobre los 10 cantones con mas accidentes 
    def grafico_top_10_cantones(self):
        top_cantones = self.df['Cantón'].value_counts().head(10)
        plt.figure(figsize=(12, 6))
        plt.barh(range(len(top_cantones)), top_cantones.values, color='coral')
        plt.yticks(range(len(top_cantones)), top_cantones.index)
        plt.title('Top 10 Cantones con Más Accidentes', fontsize=16, fontweight='bold')
        plt.xlabel('Cantidad de Accidentes', fontsize=12)
        plt.ylabel('Cantón', fontsize=12)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    #Grafico de la provincia con mas accidentes del año 2018-2024
    def grafico_provincia_mas_accidentes_por_año(self):
        años = [2018, 2020, 2022, 2024]
        provincias = []
        cantidades = []
        
        for año in años:
            datos_año = self.df[self.df['Año'] == año]
            if len(datos_año) > 0:
                provincia_max = datos_año['Provincia'].value_counts().index[0]
                cantidad_max = datos_año['Provincia'].value_counts().iloc[0]
                provincias.append(provincia_max)
                cantidades.append(cantidad_max)
            else:
                provincias.append('Sin datos')
                cantidades.append(0)
        
        plt.figure(figsize=(12, 6))
        plt.bar([str(a) for a in años], cantidades, color='purple')
        plt.title('Provincia con Más Accidentes por Año (2018-2024)', fontsize=16, fontweight='bold')
        plt.xlabel('Año', fontsize=12)
        plt.ylabel('Cantidad de Accidentes', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        # Agregar etiquetas con el nombre de la provincia
        for i, (año, provincia, cantidad) in enumerate(zip(años, provincias, cantidades)):
            plt.text(i, cantidad + cantidad*0.01, provincia, ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.show()
    
    #Grafico sobre las horas que mas ocurren accidentes
    def grafico_accidentes_por_hora(self):
        horas_validas = self.df['Hora_num'].dropna()
        horas_validas = horas_validas[(horas_validas >= 0) & (horas_validas <= 23)]
        plt.figure(figsize=(12, 6))
        plt.hist(horas_validas, bins=24, color='mediumseagreen', edgecolor='black', alpha=0.7)
        plt.title('Distribución de Accidentes por Hora del Día', fontsize=16, fontweight='bold')
        plt.xlabel('Hora del Día', fontsize=12)
        plt.ylabel('Cantidad de Accidentes', fontsize=12)
        plt.xticks(range(0, 24))
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()
