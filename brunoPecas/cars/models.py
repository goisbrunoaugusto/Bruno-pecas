from django.db import models

class CarModel(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    year = models.IntegerField()
    parts = models.ManyToManyField("parts.Part", blank=True, related_name="car_models")
    details = models.CharField(max_length=255, null=True, blank=True)

    required = ['name', 'manufacturer', 'year', 'details']

    def __str__(self):
        return f"{self.name} - {self.manufacturer} ({self.year})"