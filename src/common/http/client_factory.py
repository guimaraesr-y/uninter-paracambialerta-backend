from src.common.http.client import HttpClient, RequestsHttpClient


class HttpClientFactory:
    """Factory for creating concrete implementations of HttpClient."""

    @staticmethod
    def create() -> HttpClient:
        """
        Create a concrete implementation of HttpClient.
        """
        return RequestsHttpClient()
