import pytest
from src.location.models import Location


@pytest.fixture
def location_factory():
    def factory(
        address="address",
        number=1,
        complement="complement",
        neighborhood="neighborhood",
        city="city",
        state="state",
        latitude=0.0,
        longitude=0.0,
    ):
        return Location.objects.create(
            address=address,
            number=number,
            complement=complement,
            neighborhood=neighborhood,
            city=city,
            state=state,
            latitude=latitude,
            longitude=longitude,
        )
    return factory
