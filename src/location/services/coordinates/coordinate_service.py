from abc import ABC
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple


@dataclass
class CoordinateAddressResponse:
    number: int | None
    address: str
    neighborhood: str
    city: str
    state: str
    country: str
    full_address: str
    latitude: float
    longitude: float


class CoordinateService(ABC):

    def get_coordinates(self, address: str) -> Tuple[float, float]:
        """
        Get the coordinates for the given address.
        """
        raise NotImplementedError

    def get_address(self, latitude: Decimal, longitude: Decimal) -> Optional[CoordinateAddressResponse]:
        """
        Get the address for the given coordinates.
        """
        raise NotImplementedError
