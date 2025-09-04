from typing import Tuple
import googlemaps
from googlemaps.geocoding import geocode, reverse_geocode
import os

from src.location.services.coordinates.coordinate_service import CoordinateService


class CoordinateGoogleAdapter(CoordinateService):
    """
    Adapter for Google Maps API.
    """

    def __init__(self, api_key=os.environ.get("GOOGLE_MAPS_API_KEY")): # TODO: add secrets service
        self.client = googlemaps.Client(key=api_key)

    def get_coordinates(self, address) -> Tuple[float, float]:
        geocode_result = geocode(self.client, address)
        location = geocode_result['geometry']['location']
        return location['lat'], location['lng']

    def get_address(self, latitude, longitude):
        reverse_geocode_result = reverse_geocode(
            self.client,
            (latitude, longitude)
        )
        return reverse_geocode_result['formatted_address']
