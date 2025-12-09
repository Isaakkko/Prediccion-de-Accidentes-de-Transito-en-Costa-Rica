import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ProcesadorEDA:
    def __init__(self, archivo_crudo, archivo_limpio=None):

# Inicialización de la clase con los archivos de entrada y salida
        self.__archivo_crudo = archivo_crudo
        self.__archivo_limpio = archivo_limpio

# CSV separado por ;
        self.df = pd.read_csv(self.__archivo_crudo, sep=";", encoding="utf-8")
        self.df.columns = self.df.columns.str.strip()

    def exploracion_inicial(self):
# Primeras filas
        print("\n>>> Primeras filas:")
        print(self.df.head())

# Stats básicas
        print("\n>>> Estadísticas básicas:")
        print(self.df.describe(include="all"))

# Tipo de dato
        print("\n>>> Info del DataFrame:")
        self.df.info()

# Nulos
        print("\n>>> Valores nulos por columna:")
        print(self.df.isnull().sum())

# Columnas categóricas detectadas
        category_col = self.df.select_dtypes(include=["object"]).columns
        print("\n>>> Columnas categóricas detectadas:")
        print(list(category_col))

# Normalización de texto
        if len(category_col) > 0:
            self.df[category_col] = (
                self.df[category_col]
                .apply(lambda col: col.astype("string").str.strip().str.lower())
            )
            print("\n>>> Ejemplo columnas categóricas normalizadas:")
            print(self.df[category_col].head())

# ----------------------------------------------------------
# Conversión de día y mes
    def convertir_dia_mes(self):

# Conversión día número
        self.df["Dia_num"] = (
            self.df["Día"].astype(str)
            .str.split(".").str[0]
            .astype("Int64")
        )

# Conversión nombre del día
        self.df["Dia_nombre"] = (
            self.df["Día"].astype(str)
            .str.split(".").str[1]
            .str.strip().str.lower()
        )

# Mapeo de meses
        meses = {
            "a. enero": 1, "b. febrero": 2, "c. marzo": 3,
            "d. abril": 4, "e. mayo": 5, "f. junio": 6,
            "g. julio": 7, "h. agosto": 8, "i. setiembre": 9,
            "j. octubre": 10, "k. noviembre": 11, "l. diciembre": 12
        }

# Conversión mes número
        self.df["Mes_num"] = (
            self.df["Mes"].astype(str)
            .str.strip().str.lower()
            .map(meses)
            .astype("Int64")
        )

# ----------------------------------------------------------
# Conversión de edad
    def convertir_edad(self):
# Convertir a número
        self.df["Edad_num"] = pd.to_numeric(self.df["Edad"], errors="coerce").astype("Int64")

# ----------------------------------------------------------
# DISYUNTIVAS: Rol, Tipo lesión, Sexo, Vehículo, Provincia
    def crear_disyuntivas(self, drop_original=False):

        columnas = ["Rol", "Tipo de lesión", "Sexo", "Vehiculo en  el que viajaba", "Provincia"]

# Generación de variables disyuntivas
        dummies = pd.get_dummies(
            self.df[columnas],
            prefix=[c.replace(" ", "_").lower() for c in columnas],
            prefix_sep="_",
            drop_first=False,
            dtype="int8"
        )

# Reemplazo u unión al dataframe
        if drop_original:
            self.df = pd.concat([self.df.drop(columns=columnas), dummies], axis=1)
        else:
            self.df = pd.concat([self.df, dummies], axis=1)

        print("\nVariables disyuntivas creadas:")
        print(dummies.head())
        print("\nNúmero de nuevas columnas:", dummies.shape[1])

# ----------------------------------------------------------
# Gráficos
    def personas_por_provincia_y_rol(self):

        if "Provincia" in self.df.columns and "Rol" in self.df.columns:

# Tabla de frecuencia
            tabla = (
                self.df
                .groupby(["Provincia", "Rol"])
                .size()
                .reset_index(name="conteo")
            )

# Pivot
            pivot = tabla.pivot(index="Provincia", columns="Rol", values="conteo").fillna(0)

# Gráfico
            plt.figure(figsize=(14, 6))
            sns.heatmap(pivot, cmap="viridis")
            plt.title("Frecuencia por provincia y rol")
            plt.tight_layout()
            plt.show()

    def personas_por_edadquinquenal_y_sexo(self):

        if "Edad quinquenal" in self.df.columns and "Sexo" in self.df.columns:

# Tabla de frecuencia
            tabla = (
                self.df
                .groupby(["Edad quinquenal", "Sexo"])
                .size()
                .reset_index(name="conteo")
            )

# Pivot
            pivot = tabla.pivot(index="Edad quinquenal", columns="Sexo", values="conteo").fillna(0)

# Gráfico
            plt.figure(figsize=(10, 8))
            sns.heatmap(pivot, cmap="magma")
            plt.title("Personas por grupo de edad y sexo")
            plt.tight_layout()
            plt.show()

    def rol_vs_tipo_lesion(self):

        if "Rol" in self.df.columns and "Tipo de lesión" in self.df.columns:

# Tabla freq
            tabla = (
                self.df
                .groupby(["Rol", "Tipo de lesión"])
                .size()
                .reset_index(name="conteo")
            )

# Pivot
            pivot = tabla.pivot(index="Rol", columns="Tipo de lesión", values="conteo").fillna(0)

# Gráfico
            plt.figure(figsize=(12, 6))
            sns.heatmap(pivot, cmap="coolwarm")
            plt.title("Rol vs tipo de lesión")
            plt.tight_layout()
            plt.show()

# ----------------------------------------------------------
# Matriz de correlación
    def matriz_correlacion(self):

        df_num = self.df.select_dtypes(include=["number"])

        if not df_num.empty:
            corr = df_num.corr(numeric_only=True)

            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, cmap="coolwarm")
            plt.title("Matriz de correlación")
            plt.tight_layout()
            plt.show()

# ----------------------------------------------------------
# Guardar CSV limpio
    def guardar_dataframe(self, sep=";"):
        if self.__archivo_limpio is None:
            return

        self.df.to_csv(
            self.__archivo_limpio,
            index=False,
            sep=sep,
            encoding="utf-8-sig"
        )

        print(f"\nArchivo limpio guardado en: {self.__archivo_limpio}")
