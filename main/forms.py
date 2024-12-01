from django import forms
from django.utils import timezone
from .models import DailySchedule


class DailyScheduleForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "min": timezone.now().date().isoformat()}
        ),
        initial=timezone.now().date(),
    )

    class Meta:
        model = DailySchedule
        fields = ["date", "truck", "location"]
