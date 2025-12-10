from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

class ModeloML:
    def __init__(self): 
        self.modelo = KNeighborsClassifier(n_neighbors=8) # Usa 8 registros de accidentes historicos mas similares

    def entrenar(self, X, y):
        # Separar los datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Entrenar el modelo
        self.modelo.fit(X_train, y_train)

        # Evaluar con el 20% de datos de prueba
        predicciones = self.modelo.predict(X_test)
        accuracy = accuracy_score(y_test, predicciones)

        print("Precisión del modelo:", accuracy)
        return accuracy

    def predecir(self, nuevo_dato):
        # nuevo_dato debe ser un diccionario con las mismas columnas que X
        df = pd.DataFrame([nuevo_dato])
        pred = self.modelo.predict(df)[0]
        
        if pred == 1:
            return "accidente grave"
        else:
            return "accidente leve"

        
