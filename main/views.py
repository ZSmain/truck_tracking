from itertools import groupby
from operator import attrgetter

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import DailyScheduleForm
from .models import DailySchedule


def schedule_list(request):
    default_date = timezone.now().date()

    if request.method == "POST":
        form = DailyScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            try:
                schedule.clean()  # This will trigger model validation
                schedule.save()
                messages.success(request, "Schedule created successfully!")
                return redirect("main:schedule_list")
            except ValidationError as e:
                messages.error(request, str(e))
                form = DailyScheduleForm(request.POST)  # Preserve the form data
        else:
            if form.non_field_errors():
                messages.error(request, form.non_field_errors()[0])
    else:
        form = DailyScheduleForm()

    schedules = (
        DailySchedule.objects.filter(date__gte=default_date)
        .select_related("truck", "location")
        .order_by("date")
    )

    grouped_schedules = {
        date: list(items) for date, items in groupby(schedules, key=attrgetter("date"))
    }

    return render(
        request,
        "main/schedule_list.html",
        {
            "grouped_schedules": grouped_schedules,
            "form": form,
            "today": default_date,
        },
    )
