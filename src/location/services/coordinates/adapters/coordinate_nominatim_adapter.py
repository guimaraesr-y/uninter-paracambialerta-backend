from typing import Tuple
from src.common.http.client_factory import HttpClientFactory
from src.location.services.coordinates.coordinate_service import CoordinateService


class CoordinateNominatimAdapter(CoordinateService):

    BASE_URL = "https://nominatim.openstreetmap.org"

    def __init__(self, http_client=None):
        self.http_client = http_client or HttpClientFactory.create()

    def get_coordinates(self, address) -> Tuple[float, float]:
        params = {
            "q": address,
            "format": "json",
            "limit": 1,
        }
        try:
            response = self.http_client.get(
                f"{self.BASE_URL}/search",
                params=params
            )
            if not response:
                raise ValueError("No results found for the given address.")

            return float(response[0]["lat"]), float(response[0]["lon"])
        except (KeyError, IndexError) as e:
            raise ValueError(
                "Could not parse coordinates from the response."
            ) from e

    def get_address(self, latitude, longitude) -> str:
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
        }
        try:
            response = self.http_client.get(
                f"{self.BASE_URL}/reverse",
                params=params
            )
            if not response or "display_name" not in response:
                raise ValueError("No results found for the given coordinates.")

            return response["display_name"]
        except (KeyError, IndexError) as e:
            raise ValueError(
                "Could not parse address from the response."
            ) from e
