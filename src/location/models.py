from django.db import models

from src.location.services.coordinates.coordinate_service_factory import CoordinateServiceFactory


class Location(models.Model):
    address = models.CharField(max_length=255)
    number = models.IntegerField()
    complement = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.address}, {self.number} - {self.neighborhood}, {self.city}/{self.state}"

    def handle_geolocation(self):
        coordinate_service = CoordinateServiceFactory.create()
        self.latitude, self.longitude = coordinate_service.get_coordinates(
            self.address
        )
        self.save(update_fields=["latitude", "longitude"])
