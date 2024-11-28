from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Truck(models.Model):
    CUISINE_CHOICES = [
        ("MEX", "Mexican"),
        ("DZ", "Algerian"),
        ("ITA", "Italian"),
        ("JPN", "Japanese"),
        ("IND", "Indian"),
        ("CHI", "Chinese"),
        ("VGT", "Vegetarian"),
    ]

    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=3, choices=CUISINE_CHOICES)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class DailySchedule(models.Model):
    date = models.DateField(default=timezone.now)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ("date", "location"),
            ("date", "truck"),
        )

    def clean(self):
        # Prevent double booking of locations
        if (
            DailySchedule.objects.filter(date=self.date, location=self.location)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                "This location is already booked for the selected date."
            )

        # Prevent a truck from being at multiple locations on the same day
        if (
            DailySchedule.objects.filter(date=self.date, truck=self.truck)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                "This truck is already scheduled for the selected date."
            )

    def __str__(self):
        return f"{self.truck.name} at {self.location.name} on {self.date}"
