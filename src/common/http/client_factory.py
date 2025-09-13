from typing import Optional
from src.common.http.client import HttpClient, RequestsHttpClient


class HttpClientFactory:
    """Factory for creating concrete implementations of HttpClient."""

    @staticmethod
    def create(user_agent: Optional[str] = None) -> HttpClient:
        """
        Create a concrete implementation of HttpClient.
        """
        return RequestsHttpClient(user_agent=user_agent)
