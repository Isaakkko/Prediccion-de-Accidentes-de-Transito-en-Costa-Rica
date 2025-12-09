import pandas as pd                         # Librerias vistas en clase
from sqlalchemy import create_engine         # sqlalchemy para base de datos 

class GestorBaseDatos:
    def __init__(self, ruta_db="accidentes.db"):         # Aqui se crea el engine del sqlalchemy para usar sqlite 
        self.engine = create_engine(f"sqlite:///{ruta_db}") 

    def crear_tabla_desde_csv(self, nombre_tabla, ruta_csv):  # Aqui se usa el csv de accidentes
        df = pd.read_csv(ruta_csv)     # Ruta csv
        df.to_sql(nombre_tabla, self.engine, if_exists="replace", index=False) # Se hace el dataframe en la base de datos
        return df   # Devuelve el dataframe útil

    def ejecutar_consulta(self, sql):  # Metodo para hacer una consulta SQL
        return pd.read_sql(sql, self.engine)   # Y devuelve un dataframe como resultado 
       
