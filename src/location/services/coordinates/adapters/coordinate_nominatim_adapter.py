from typing import Tuple
from src.location.services.coordinates.coordinate_service import CoordinateService


class CoordinateNominatimAdapter(CoordinateService):

    def get_coordinates(self, address) -> Tuple[float, float]:
        pass  # TODO: Implement

    def get_address(self, latitude, longitude) -> str:
        pass  # TODO: Implement
