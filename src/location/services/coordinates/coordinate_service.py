from abc import ABC

from src.location.services.coordinates.adapters.coordinate_google_adapter import CoordinateGoogleAdapter


class CoordinateService(ABC):
    def __init__(self):
        pass

    def get_coordinates(self, address):
        """
        Get the coordinates for the given address.
        """
        raise NotImplementedError

    def get_address(self, latitude, longitude):
        """
        Get the address for the given coordinates.
        """
        raise NotImplementedError


coordinate_service = CoordinateGoogleAdapter
