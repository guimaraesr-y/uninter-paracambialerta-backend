from rest_framework import serializers

from src.location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "formatted_address",
            "latitude",
            "longitude",
        ]
