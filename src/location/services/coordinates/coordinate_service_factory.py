from typing import Optional
from src.location.services.coordinates.adapters import CoordinateNominatimAdapter
from src.location.services.coordinates.coordinate_service import CoordinateService


class CoordinateServiceFactory:
    """Factory for creating concrete implementations of CoordinateService."""

    @staticmethod
    def create(service_type: Optional[str] = None) -> CoordinateService:
        """
        Create a concrete implementation of CoordinateService based on
        service_type.
        """
        if not service_type or service_type == "nominatim":
            return CoordinateNominatimAdapter()

        raise ValueError(f"Invalid service type: {service_type}")
