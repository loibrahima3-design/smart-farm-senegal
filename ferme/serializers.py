from rest_framework import serializers
from .models import Culture, Parcelle, Capteur


class CultureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Culture
        fields = "__all__"


class ParcelleSerializer(serializers.ModelSerializer):

    culture = CultureSerializer(read_only=True)

    class Meta:
        model = Parcelle
        fields = "__all__"


class CapteurSerializer(serializers.ModelSerializer):

    parcelle = serializers.StringRelatedField()

    class Meta:
        model = Capteur
        fields = "__all__"