from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Truck, Location, DailySchedule


class DailyScheduleTest(TestCase):
    def setUp(self):
        # Create test trucks
        self.truck1 = Truck.objects.create(name="Taco Truck", cuisine="MEX")
        self.truck2 = Truck.objects.create(name="Pasta Truck", cuisine="ITA")

        # Create test locations
        self.location1 = Location.objects.create(
            name="Downtown Plaza", address="123 Main St"
        )
        self.location2 = Location.objects.create(
            name="Tech Park", address="456 Innovation Ave"
        )

        # Set test date
        self.today = timezone.now().date()

    def test_valid_schedule(self):
        """Test creating a valid schedule"""
        schedule = DailySchedule(
            date=self.today, truck=self.truck1, location=self.location1
        )
        schedule.clean()  # Should not raise ValidationError
        schedule.save()
        self.assertEqual(DailySchedule.objects.count(), 1)

    def test_location_conflict(self):
        """Test that a location cannot be double-booked"""
        # Create first schedule
        DailySchedule.objects.create(
            date=self.today, truck=self.truck1, location=self.location1
        )

        # Attempt to create conflicting schedule
        conflicting_schedule = DailySchedule(
            date=self.today, truck=self.truck2, location=self.location1
        )

        with self.assertRaises(ValidationError):
            conflicting_schedule.clean()  # Should raise ValidationError

    def test_truck_conflict(self):
        """Test that a truck cannot be scheduled twice in one day"""
        # Create first schedule
        DailySchedule.objects.create(
            date=self.today, truck=self.truck1, location=self.location1
        )

        # Attempt to schedule same truck at different location
        conflicting_schedule = DailySchedule(
            date=self.today, truck=self.truck1, location=self.location2
        )

        with self.assertRaises(ValidationError):
            conflicting_schedule.clean()  # Should raise ValidationError

    def test_different_dates_allowed(self):
        """Test that same truck and location can be scheduled on different dates"""
        # Create schedule for today
        DailySchedule.objects.create(
            date=self.today, truck=self.truck1, location=self.location1
        )

        # Schedule same truck and location for tomorrow
        tomorrow = self.today + timezone.timedelta(days=1)
        next_day_schedule = DailySchedule(
            date=tomorrow, truck=self.truck1, location=self.location1
        )

        next_day_schedule.clean()  # Should not raise ValidationError
        next_day_schedule.save()
        self.assertEqual(DailySchedule.objects.count(), 2)
