from django.urls import path
from .views import (
    accueil,
    cultures,
    parcelles,
    dashboard,
    rentabilite,
    carte,
    capteurs,
    prediction,
    CultureListAPI,
    ParcelleListAPI,
    CapteurListAPI,
)

urlpatterns = [
    path("", accueil, name="accueil"),
    path("cultures/", cultures, name="cultures"),
    path("parcelles/", parcelles, name="parcelles"),
    path("dashboard/", dashboard, name="dashboard"),
    path("rentabilite/", rentabilite, name="rentabilite"),
    path("carte/", carte, name="carte"),
    path("capteurs/", capteurs, name="capteurs"),
    path("prediction/", prediction, name="prediction"),

    path("api/cultures/", CultureListAPI.as_view()),
    path("api/parcelles/", ParcelleListAPI.as_view()),
    path("api/capteurs/", CapteurListAPI.as_view()),
]