from django.contrib import admin
from .models import Truck, Location, DailySchedule


class TruckAdmin(admin.ModelAdmin):
    list_display = ("name", "cuisine")


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


class DailyScheduleAdmin(admin.ModelAdmin):
    list_display = ("date", "truck", "location")


admin.site.register(Truck, TruckAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(DailySchedule, DailyScheduleAdmin)
