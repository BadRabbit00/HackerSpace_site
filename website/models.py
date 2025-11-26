from django.db import models

class SiteSettings(models.Model):
    address = models.CharField(max_length=255)
    working_hours = models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"HackerSpace Info at {self.address}"
