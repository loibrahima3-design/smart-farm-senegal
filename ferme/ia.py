from sklearn.linear_model import LinearRegression
import numpy as np


# ===== Données d'entraînement (exemple) =====
# [superficie, eau, azote, phosphore, potassium]

X = np.array([
    [1, 80, 30, 20, 20],
    [2, 100, 40, 25, 30],
    [3, 120, 50, 30, 40],
    [4, 140, 60, 35, 50],
    [5, 160, 70, 40, 60],
])

# Rendement correspondant (tonnes)
y = np.array([2, 4, 6, 8, 10])


# ===== Entraînement du modèle =====
modele = LinearRegression()
modele.fit(X, y)


def predire_rendement(
    superficie,
    eau,
    azote,
    phosphore,
    potassium
):
    entree = np.array([
        [superficie, eau, azote, phosphore, potassium]
    ])

    prediction = modele.predict(entree)

    return round(float(prediction[0]), 2)