from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from courts.models import Court
from .forms import BookingForm
from .models import Booking


@login_required
def create_booking(request, court_id):
    court = get_object_or_404(Court, id=court_id, is_active=True)

    if request.method == "POST":
        form = BookingForm(request.POST, court=court)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.court = court

            try:
                with transaction.atomic():
                    booking.save()

                messages.success(request, "Your booking was created successfully!")
                return redirect("court_detail", court_id=court.id)

            except IntegrityError:
                messages.error(
                    request,
                    "Sorry, this time slot has just been booked. Please choose another one."
                )
    else:
        form = BookingForm(court=court)

    return render(request, "bookings/create_booking.html", {
        "form": form,
        "court": court,
    })


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("court", "time_slot", "court__sport_center")
        .order_by("-time_slot__date", "-time_slot__start_time")
    )

    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings
    })

