from django import forms
from .models import DailySchedule


class DailyScheduleForm(forms.ModelForm):
    class Meta:
        model = DailySchedule
        fields = ["truck", "location"]
