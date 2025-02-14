from django.db import models

class Part(models.Model):
    part_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    required = ['name', 'price', 'quantity', 'part_number']
    def __str__(self):
        return f"{self.part_number} - {self.name}"