from src.reports.urls import urlpatterns as report_urls
from src.users.urls import urlpatterns as user_urls


urlpatterns = [
    *report_urls,
    *user_urls,
]
