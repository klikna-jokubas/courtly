from django.contrib import admin
from .models import (
    SportType,
    Address,
    SportCenter,
    Court,
    OpeningHours
)

admin.site.register(SportType)
admin.site.register(Address)
admin.site.register(SportCenter)
admin.site.register(Court)
admin.site.register(OpeningHours)