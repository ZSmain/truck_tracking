from django.shortcuts import render
from .models import DailySchedule
from django.utils import timezone

# Create your views here.


def todays_schedule(request):
    today = timezone.now().date()
    schedules = DailySchedule.objects.filter(date=today).select_related(
        "truck", "location"
    )
    return render(request, "main/todays_schedule.html", {"schedules": schedules})
