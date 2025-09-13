from enum import Enum
import os
from typing import Optional

from src.location.services.coordinates.adapters import CoordinateNominatimAdapter
from src.location.services.coordinates.adapters.coordinate_google_adapter import CoordinateGoogleAdapter
from src.location.services.coordinates.coordinate_service import CoordinateService


class CoordinateServiceType(Enum):
    GOOGLE = "google"
    NOMINATIM = "nominatim"


class CoordinateServiceFactory:
    """Factory for creating concrete implementations of CoordinateService."""

    @staticmethod
    def create(service_type: Optional[CoordinateServiceType] = None) -> CoordinateService:
        """
        Create a concrete implementation of CoordinateService based on
        service_type.
        """
        if not service_type or service_type == "google":
            return CoordinateGoogleAdapter(key=os.environ.get("GOOGLE_MAPS_API_KEY"))
        if service_type == "nominatim":
            return CoordinateNominatimAdapter()

        raise ValueError(f"Invalid service type: {service_type}")
