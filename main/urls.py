from django.urls import path
from main import views

urlpatterns = [
    path("schedule/today/", views.todays_schedule, name="todays_schedule"),
]
