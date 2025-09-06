from abc import ABC
from typing import Tuple


class CoordinateService(ABC):

    def get_coordinates(self, address) -> Tuple[float, float]:
        """
        Get the coordinates for the given address.
        """
        raise NotImplementedError

    def get_address(self, latitude, longitude) -> str:
        """
        Get the address for the given coordinates.
        """
        raise NotImplementedError
