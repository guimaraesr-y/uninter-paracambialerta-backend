import os
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    PRODUCTION = 'production'
    STAGING = 'staging'
    DEVELOPMENT = 'development'
    TEST = 'test'


@dataclass
class EnvironmentVariables:
    GOOGLE_MAPS_API_KEY: str
    ENVIRONMENT: str


class EnvironmentService:
    """
    Class responsible for managing the environment.

    Provides methods to load environment variables from a .env file and to get the current environment.
    """

    @staticmethod
    def load_env():
        from dotenv import load_dotenv
        load_dotenv()

    @staticmethod
    def get_variables():
        return EnvironmentVariables(
            GOOGLE_MAPS_API_KEY=os.environ.get('GOOGLE_MAPS_API_KEY', ''),
            ENVIRONMENT=EnvironmentService.get_environment().value
        )

    @staticmethod
    def get(variable: str) -> str:
        return os.environ.get(variable, "")

    @staticmethod
    def get_environment():
        return Environment(os.environ.get('ENVIRONMENT', 'development'))

    @staticmethod
    def is_production():
        return EnvironmentService.get_environment() == Environment.PRODUCTION
