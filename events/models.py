from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    subscription_type = models.CharField(max_length=100)  # e.g., free, resident_temp, resident_perm
    

    def __str__(self):
        return self.title