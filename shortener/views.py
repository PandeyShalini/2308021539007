from rest_framework import status,generics
from rest_framework.response import Response
from django.utils import timezone
from .models import ShortURL, Click
from .serializers import ShortURLSerializer, ClickSerializer
from django.shortcuts import get_object_or_404
import string,random

def generate_shortcode(length=6):
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters)for _ in range(length))

class CreateShortURL(generics.CreateAPIView):
    serializer_class = ShortURLSerializer

    def post(self, request, *args, **kwargs):
        url = request.data.get('url')
        validity_days = int(request.data.get('validity_days', 30))
        shortcode = request.data.get('shortcode') or generate_shortcode()
        now = timezone.now()
        expiry = now + timezone.timedelta(days=validity_days)
        ShortURL.objects.create(
            original_url=url,
            short_code=shortcode,
            created_at=now,
            expires_at=expiry
        )
        res = {
           'shortLink': f"http://localhost:8000/{shortcode}",
           'expiry': expiry.isoformat()
        }
        return Response(res, status=status.HTTP_201_CREATED)

class URLStatsView(generics.RetrieveAPIView):
    def get(self, request, shortcode):
        url_obj = get_object_or_404(ShortURL, short_code=shortcode)
        stats = {
            'total_clicks': url_obj.clicks_data.count(),
            'orginial_url': url_obj.original_url,
            'creation_date': url_obj.created_at,
            'expiry':url_obj.expires_at,
            'click_details': ClickSerializer(url_obj.clicks_data, many=True).data
        }
    
        return Response(stats)