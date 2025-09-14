from typing import Any, Dict, List, Optional
import googlemaps
from googlemaps.geocoding import geocode, reverse_geocode
from src.location.services.coordinates.coordinate_service import CoordinateAddressResponse, CoordinateService


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
        if not reverse_geocode_result:
            return None
        return self._parse_geocode_result(reverse_geocode_result[0])

    @staticmethod
    def _find_component(components: List[Dict[str, Any]], wanted_types: List[str]) -> Optional[str]:
        """
        Find the first component whose `types` contains any type in `wanted_types`.
        Return `long_name` or None.
        """
        for comp in components:
            types = comp.get("types", [])
            if any(t in types for t in wanted_types):
                return comp.get("long_name")
        return None

    def _parse_geocode_result(self, result: Dict[str, Any]) -> CoordinateAddressResponse:
        """
        Extrai os campos relevantes do resultado do Google Geocoding.
        """
        components = result.get("address_components", [])
        formatted = result.get("formatted_address")

        # número
        number_str = self._find_component(components, ["street_number"])
        number = None
        if number_str:
            try:
                number = int(number_str)
            except (ValueError, TypeError):
                # alguns números podem conter letras (ex: '125A') -> keep None ou tentar extrair dígitos
                digits = ''.join(ch for ch in str(number_str) if ch.isdigit())
                if digits:
                    try:
                        number = int(digits)
                    except ValueError:
                        number = None

        address = self._find_component(components, ["route", "street_address", "premise"])
        if not address:
            # fallback: use formatted_address first segment
            if formatted:
                address = formatted.split(",")[0].strip()

        neighborhood = self._find_component(components, ["sublocality_level_1", "neighborhood", "sublocality"])
        city = self._find_component(components, [
            "administrative_area_level_2",
            "locality",
            "postal_town",
        ])

        state = self._find_component(components, ["administrative_area_level_1"])
        country = self._find_component(components, ["country"])

        geom = result.get("geometry", {}).get("location", {})
        lat = geom.get("lat")
        lng = geom.get("lng")

        return CoordinateAddressResponse(
            number=number,
            address=address or "",
            neighborhood=neighborhood or "",
            city=city or "",
            state=state or "",
            country=country or "",
            full_address=formatted or "",
            latitude=lat,
            longitude=lng,
        )
