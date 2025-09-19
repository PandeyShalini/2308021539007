from django.urls import path
from .views import CreateShortURL, URLStatsView

urlpatterns = [
    path('shorturls/', CreateShortURL.as_view(), name='create_short_url'),
    path('shorturls/<str:shortcode>/stats/', URLStatsView.as_view(), name='url_stats'),
]
