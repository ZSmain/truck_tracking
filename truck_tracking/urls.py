from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schedule/today/", views.todays_schedule, name="todays_schedule"),
]