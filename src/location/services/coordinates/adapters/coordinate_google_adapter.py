import googlemaps
from googlemaps.geocoding import geocode, reverse_geocode
from src.location.services.coordinates.coordinate_service import CoordinateService


class CoordinateGoogleAdapter(CoordinateService):

    __slots__ = ('_key', '_gmaps')

    def __init__(self, key):
        self._key = key
        self._gmaps = googlemaps.Client(key=self._key)

    def get_coordinates(self, address):
        geocode_result = geocode(client=self._gmaps, address=address)
        lat, lng = (
            geocode_result[0]['geometry']['location']['lat'],
            geocode_result[0]['geometry']['location']['lng']
        )
        return lat, lng

    def get_address(self, latitude, longitude):
        reverse_geocode_result = reverse_geocode(client=self._gmaps, latlng=(latitude, longitude))
        return reverse_geocode_result[0]['formatted_address']
