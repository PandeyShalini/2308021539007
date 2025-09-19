from django.db import models
class ShortURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)


class Click(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    timpstamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.CharField(max_length=255, null=True, blank=True)
