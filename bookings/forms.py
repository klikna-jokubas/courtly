from django import forms
from django.db.models import Q
from django.utils import timezone

from .models import Booking, TimeSlot


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ["time_slot"]

        widgets = {
            "time_slot": forms.Select(
                attrs={"class": "form-select"}
            )
        }

    
    def __init__(self, *args, court=None, booking=None, **kwargs):
        super().__init__(*args, **kwargs)

        now = timezone.localtime()

        available_slots = TimeSlot.objects.filter(
            court=court
        ).filter(
            Q(date__gt=now.date()) |
            Q(date=now.date(), start_time__gt=now.time())
        ).exclude(
            bookings__status__in=[
                Booking.BookingStatus.PENDING,
                Booking.BookingStatus.CONFIRMED,
            ]
        )

        # During rescheduling, also allow the booking's current slot.
        if booking:
            available_slots = available_slots | TimeSlot.objects.filter(
                id=booking.time_slot_id
            )

        self.fields["time_slot"].queryset = available_slots.distinct().order_by(
            "date", "start_time"
        )

        self.fields["time_slot"].label = "Available time slots"

