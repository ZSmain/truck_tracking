from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q


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
        if self.id:
            conflicts = (
                DailySchedule.objects.filter(
                    Q(date=self.date)
                    & (Q(location=self.location) | Q(truck=self.truck))
                )
                .exclude(id=self.id)
                .exists()
            )
        else:
            conflicts = DailySchedule.objects.filter(
                Q(date=self.date) & (Q(location=self.location) | Q(truck=self.truck))
            ).exists()

        if conflicts:
            raise ValidationError(
                "Schedule conflict: The selected location or truck is already booked for this date."
            )

    def __str__(self):
        return f"{self.truck.name} at {self.location.name} on {self.date}"
