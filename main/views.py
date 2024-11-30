from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import DailySchedule
from .forms import DailyScheduleForm
from django.utils import timezone

# Create your views here.


def todays_schedule(request):
    today = timezone.now().date()

    if request.method == "POST":
        form = DailyScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.date = today
            try:
                schedule.clean()
                schedule.save()
                messages.success(request, "Schedule created successfully!")
                return redirect("todays_schedule")
            except ValidationError as e:
                messages.error(request, e.message)
        else:
            # Handle specific form field errors
            for field, errors in form.errors.items():
                if field == "__all__":
                    messages.error(request, errors[0])
                else:
                    messages.error(request, f"{field.title()}: {errors[0]}")
    else:
        form = DailyScheduleForm()

    schedules = DailySchedule.objects.filter(date=today).select_related(
        "truck", "location"
    )
    return render(
        request, "main/todays_schedule.html", {"schedules": schedules, "form": form}
    )
