from django.db import models


class Culture(models.Model):
    nom = models.CharField(max_length=100)

    besoin_eau = models.FloatField(default=0)
    azote = models.FloatField(default=0)
    phosphore = models.FloatField(default=0)
    potassium = models.FloatField(default=0)

    def __str__(self):
        return self.nom


class Parcelle(models.Model):
    nom = models.CharField(max_length=100)
    superficie = models.FloatField()

    # NOUVEAUX CHAMPS GPS
    latitude = models.FloatField(default=14.6937)
    longitude = models.FloatField(default=-17.4441)

    culture = models.ForeignKey(
        Culture,
        on_delete=models.CASCADE
    )

    def cout_eau(self):
        return self.superficie * self.culture.besoin_eau * 50

    def cout_engrais(self):
        total_npk = (
            self.culture.azote
            + self.culture.phosphore
            + self.culture.potassium
        )
        return self.superficie * total_npk * 100

    def cout_main_oeuvre(self):
        return self.superficie * 20000

    def revenu_estime(self):
        return self.superficie * 300000

    def benefice(self):
        return (
            self.revenu_estime()
            - self.cout_eau()
            - self.cout_engrais()
            - self.cout_main_oeuvre()
        )

    def __str__(self):
        return self.nom
class Capteur(models.Model):

    TYPES = [
        ("temperature", "Température"),
        ("humidite", "Humidité"),
        ("luminosite", "Luminosité"),
    ]

    nom = models.CharField(max_length=100)

    type_capteur = models.CharField(
        max_length=20,
        choices=TYPES
    )

    valeur = models.FloatField()

    date_mesure = models.DateTimeField(
        auto_now_add=True
    )

    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.nom} ({self.type_capteur})"