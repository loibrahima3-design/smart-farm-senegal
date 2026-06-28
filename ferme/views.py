from .ia import predire_rendement
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CultureSerializer,
    ParcelleSerializer,
    CapteurSerializer
)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Culture, Parcelle, Capteur
import json
import requests


def accueil(request):
    cultures = Culture.objects.all()

    return render(request, "ferme/accueil.html", {
        "cultures": cultures
    })


def cultures(request):
    cultures = Culture.objects.all()

    return render(request, "ferme/cultures.html", {
        "cultures": cultures
    })


def parcelles(request):
    parcelles = Parcelle.objects.all()

    return render(request, "ferme/parcelles.html", {
        "parcelles": parcelles
    })


@login_required
def dashboard(request):

    # ===== MÉTÉO DE DAKAR =====

    meteo = {
        "temperature": "N/A",
        "vent": "N/A"
    }

    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=14.6937"
            "&longitude=-17.4441"
            "&current=temperature_2m,wind_speed_10m"
        )

        reponse = requests.get(url, timeout=5)
        donnees = reponse.json()

        meteo["temperature"] = donnees["current"]["temperature_2m"]
        meteo["vent"] = donnees["current"]["wind_speed_10m"]

    except Exception as e:
        print("Erreur météo :", e)

    # ===== STATISTIQUES =====

    nb_cultures = Culture.objects.count()
    nb_parcelles = Parcelle.objects.count()

    surface_totale = sum(
        p.superficie for p in Parcelle.objects.all()
    )

    parcelles_db = Parcelle.objects.all()

    noms = [p.nom for p in parcelles_db]
    superficies = [float(p.superficie) for p in parcelles_db]

    # ===== IA V3 =====

    recommandations = []

    for culture in Culture.objects.all():

        conseils = []

        # Analyse agronomique
        if culture.besoin_eau > 100:
            conseils.append("💧 Forte irrigation recommandée.")
        elif culture.besoin_eau > 70:
            conseils.append("💦 Irrigation modérée recommandée.")
        else:
            conseils.append("☀️ Culture adaptée aux zones peu arrosées.")

        if culture.azote > 80:
            conseils.append("🧪 Besoin élevé en azote (N).")
        elif culture.azote > 40:
            conseils.append("🌱 Besoin moyen en azote.")

        if culture.phosphore < 20:
            conseils.append("⚠️ Complément phosphaté conseillé.")

        if culture.potassium > 40:
            conseils.append("🍌 Besoin important en potassium (K).")

        # Analyse météo
        temperature = meteo.get("temperature", 0)
        vent = meteo.get("vent", 0)

        if isinstance(temperature, (int, float)):

            if temperature > 35:
                conseils.append(
                    "🔥 Température élevée : augmenter l'irrigation."
                )

            elif temperature < 20:
                conseils.append(
                    "🌡️ Température basse : surveiller la croissance."
                )

        if isinstance(vent, (int, float)):

            if vent > 30:
                conseils.append(
                    "💨 Vent fort : reporter l'épandage des engrais."
                )

        recommandations.append({
            "nom": culture.nom,
            "conseils": conseils
        })

    return render(request, "ferme/dashboard.html", {
        "nb_cultures": nb_cultures,
        "nb_parcelles": nb_parcelles,
        "surface_totale": surface_totale,
        "noms": json.dumps(noms),
        "superficies": json.dumps(superficies),
        "recommandations": recommandations,
        "meteo": meteo,
    })


@login_required
def rentabilite(request):

    donnees = []

    for p in Parcelle.objects.all():

        donnees.append({
            "nom": p.nom,
            "cout_eau": p.cout_eau(),
            "cout_engrais": p.cout_engrais(),
            "cout_main_oeuvre": p.cout_main_oeuvre(),
            "revenu": p.revenu_estime(),
            "benefice": p.benefice(),
        })

    return render(request, "ferme/rentabilite.html", {
        "donnees": donnees
    })
@login_required
def carte(request):

    parcelles = Parcelle.objects.all()

    return render(request, "ferme/carte.html", {
        "parcelles": parcelles
    })
@login_required
def capteurs(request):

    capteurs = Capteur.objects.all()

    recommandations = []

    for c in capteurs:

        conseil = ""

        if c.type_capteur == "humidite":

            if c.valeur < 30:
                conseil = "💧 Humidité faible : lancer l'irrigation."
            else:
                conseil = "✅ Humidité correcte."

        elif c.type_capteur == "temperature":

            if c.valeur > 38:
                conseil = "🔥 Température élevée : protéger les cultures."
            else:
                conseil = "✅ Température normale."

        elif c.type_capteur == "luminosite":

            if c.valeur < 300:
                conseil = "☁️ Luminosité faible : surveiller la météo."
            else:
                conseil = "☀️ Luminosité satisfaisante."

        recommandations.append({
            "capteur": c,
            "conseil": conseil
        })

    return render(request, "ferme/capteurs.html", {
        "recommandations": recommandations
    })
# ===== API REST SÉCURISÉE =====

class CultureListAPI(generics.ListAPIView):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer
    permission_classes = [IsAuthenticated]


class ParcelleListAPI(generics.ListAPIView):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer
    permission_classes = [IsAuthenticated]


class CapteurListAPI(generics.ListAPIView):
    queryset = Capteur.objects.all()
    serializer_class = CapteurSerializer
    permission_classes = [IsAuthenticated]
    @login_required
def prediction(request):

    resultat = None

    if request.method == "POST":

        superficie = float(request.POST["superficie"])
        eau = float(request.POST["eau"])
        azote = float(request.POST["azote"])
        phosphore = float(request.POST["phosphore"])
        potassium = float(request.POST["potassium"])

        resultat = predire_rendement(
            superficie,
            eau,
            azote,
            phosphore,
            potassium
        )

    return render(
        request,
        "ferme/prediction.html",
        {
            "resultat": resultat
        }
    )