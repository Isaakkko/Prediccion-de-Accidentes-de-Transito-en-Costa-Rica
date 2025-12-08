import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ProcesadorEDA:
    def __init__(self, archivo_crudo, archivo_limpio=None):

# Inicialización de la clase con los archivos de entrada y salida
        self.__archivo_crudo = archivo_crudo
        self.__archivo_limpio = archivo_limpio

# CSV SEPARADO POR ;
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

# Número de filas y columnas
        print("\n>>> Dimensiones (filas, columnas):")
        print(self.df.shape)

# Nulos
        print("\n>>> Valores nulos por columna:")
        print(self.df.isnull().sum())

# Normalizar las columnas categóricas
        category_col = self.df.select_dtypes(include=["object"]).columns
        print("\n>>> Columnas categóricas detectadas:")
        print(list(category_col))

        if len(category_col) > 0:
# Limpiar espacios y pasar a minúsculas, ignorando NaN
            self.df[category_col] = (
                self.df[category_col]
                .apply(lambda col: col.astype("string").str.strip().str.lower())
            )
            print("\n>>> Ejemplo columnas categóricas normalizadas:")
            print(self.df[category_col].head())
#Conversiones a numericos
    def convertir_dia_mes(self):
        self.df["Dia_num"] = (
            self.df["Día"].astype(str)
            .str.split(".").str[0]
            .astype("Int64")
        )

        self.df["Dia_nombre"] = (
            self.df["Día"].astype(str)
            .str.split(".").str[1]
            .str.strip().str.lower()
        )

        meses = {
            "A. Enero": 1, "B. Febrero": 2, "C. Marzo": 3,
            "D. Abril": 4, "E. Mayo": 5, "F. Junio": 6,
            "G. Julio": 7, "H. Agosto": 8, "I. Setiembre": 9,
            "J. Octubre": 10, "K. Noviembre": 11, "L. Diciembre": 12
        }

        self.df["Mes_num"] = (
            self.df["Mes"].astype(str)
            .str.strip().map(meses)
            .astype("Int64")
        )
# ----------------------------------------------------------
#  Clase de accidente DISYUNTIVA
#  Rural o urbano DISYUNTIVA
#  Calzada vertircal DISYUNTIVA
#  Calzada horizontal DISYUNTIVA

    def crear_disyuntivas(self, drop_original=False):
        columnas = ["Clase de accidente",
                    "Rural o urbano",
                    "Calzada vertical",
                    "Calzada horizontal"]

        dummies = pd.get_dummies(
            self.df[columnas],
            prefix=["accidente", "clima", "calzada", "ruta"],
            prefix_sep="_",
            drop_first=False,
            dtype="int8"
        )

        if drop_original:
            self.df = pd.concat(
                [self.df.drop(columns=columnas), dummies],
                axis=1
            )
        else:
            self.df = pd.concat([self.df, dummies], axis=1)

        print("\nVariables disyuntivas:")
        print(dummies.head())
        print("\nNúmero de columnas nuevas:", dummies.shape[1])

# ----------------------------------------------------------
# GRAFICOS
    def frecuencia_provincia_hora(self):
        if "Hora_num" not in self.df.columns:
            self.df["Hora"] = self.df["Hora"].astype(str).str.slice(0, 5)
            self.df["Hora"] = pd.to_datetime(self.df["Hora"], format="%H:%M", errors="coerce")
            self.df["Hora_num"] = self.df["Hora"].dt.hour.astype("Int64")

        if "Provincia" in self.df.columns and "Hora_num" in self.df.columns:
            tabla = (
                self.df
                .groupby(["Provincia", "Hora_num"])
                .size()
                .reset_index(name="conteo")
            )

            pivot = tabla.pivot(index="Provincia", columns="Hora_num", values="conteo").fillna(0)

            plt.figure(figsize=(14, 6))
            sns.heatmap(pivot, cmap="viridis")
            plt.title("Frecuencia de accidentes por provincia y hora del día")
            plt.xlabel("Hora del día")
            plt.ylabel("Provincia")
            plt.tight_layout()
            plt.show()

    def mapa_calor_zona(self):
        if "Región Mideplan" in self.df.columns and "Tipo ruta" in self.df.columns:
            tabla = (
                self.df
                .groupby(["Región Mideplan", "Tipo ruta"])
                .size()
                .reset_index(name="conteo")
            )

            pivot = tabla.pivot(index="Región Mideplan", columns="Tipo ruta", values="conteo").fillna(0)

            plt.figure(figsize=(10, 6))
            sns.heatmap(pivot, cmap="magma")
            plt.title("Mapa de calor de accidentes por zona")
            plt.xlabel("Tipo de ruta")
            plt.ylabel("Región Mideplan")
            plt.tight_layout()
            plt.show()

    def accidente_vs_clima(self):
        if "Clase de accidente" in self.df.columns and "Estado del tiempo" in self.df.columns:
            tabla = (
                self.df
                .groupby(["Clase de accidente", "Estado del tiempo"])
                .size()
                .reset_index(name="conteo")
            )

            pivot = tabla.pivot(index="Clase de accidente", columns="Estado del tiempo", values="conteo").fillna(0)

            plt.figure(figsize=(12, 6))
            sns.heatmap(pivot, cmap="coolwarm")
            plt.title("Tipos de accidentes vs condiciones climáticas")
            plt.xlabel("Estado del tiempo")
            plt.ylabel("Clase de accidente")
            plt.tight_layout()
            plt.show()

    def matriz_correlacion(self):
        df_num = self.df.select_dtypes(include=["number"])
        if not df_num.empty:
            corr = df_num.corr()

            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
            plt.title("Matriz de correlación entre variables numéricas")
            plt.tight_layout()
            plt.show()

#-------------
    def guardar_dataframe(self):
        if self.__archivo_limpio is None:
            return
        self.df.to_csv(self.__archivo_limpio, index=False, encoding="utf-8")
        print(f"Archivo limpio guardado en: {self.__archivo_limpio}")
