from django.db import models

class QRCode(models.Model):
    url = models.URLField(max_length=200)
    edit_code = models.CharField(max_length=10, unique=True)
    security_code = models.CharField(max_length=10, unique=True)
    file_url = models.URLField(max_length=200, blank=True, null=True)
