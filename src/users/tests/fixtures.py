import pytest

from src.users.models import BasicUser


@pytest.fixture
def user():
    return BasicUser.objects.create_user(
        first_name="John Doe",
        last_name="Doe",
        username="johndoe",
        email="johndoe@example.com",
    )
