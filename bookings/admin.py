from django.contrib import admin
from .models import TimeSlot, Booking, Payment

admin.site.register(TimeSlot)
admin.site.register(Booking)
admin.site.register(Payment)