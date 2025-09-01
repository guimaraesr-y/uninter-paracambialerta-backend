from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=255)
    number = models.IntegerField()
    complement = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    def __str__(self):
        return f"{self.address}, {self.number} - {self.neighborhood}, {self.city}/{self.state}"
