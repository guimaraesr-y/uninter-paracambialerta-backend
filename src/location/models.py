from decimal import Decimal
import os
from django.db import models

from src.common.services import EnvironmentService
from src.location.services.coordinates.coordinate_service_factory import (
    CoordinateServiceFactory
)


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
        return self.formatted_address

    @property
    def formatted_address(self) -> str:
        if not self.address or not self.number or not self.neighborhood or not self.city or not self.state:
            return ''
        return f'{self.address}, {self.number} - {self.neighborhood}, {self.city}, {self.state}'

    def save(self, *args, **kwargs) -> None:
        self.handle_geolocation()
        return super().save(*args, **kwargs)

    def handle_geolocation(self):
        if not EnvironmentService.is_production():
            return

        self._get_address_from_coordinates()
        self._get_coordinates_from_address()

    def _get_address_from_coordinates(self):
        if not self.latitude or not self.longitude or self.formatted_address:
            return

        coordinate_service = self._get_coordinate_service()
        address = coordinate_service.get_address(
            Decimal(self.latitude),
            Decimal(self.longitude),
        )

        if not address:
            return

        self.address = address.address
        self.number = address.number
        self.neighborhood = address.neighborhood
        self.city = address.city
        self.state = address.state

    def _get_coordinates_from_address(self):
        if not self.address or self.latitude or self.longitude:
            return

        coordinate_service = self._get_coordinate_service()
        self.latitude, self.longitude = coordinate_service.get_coordinates(
            self.address
        )

    def _get_coordinate_service(self):
        return CoordinateServiceFactory.create()
