from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from decimal import Decimal

from courts.models import Court
from .forms import BookingForm
from .models import Booking, Payment



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

                    # Calculate booking duration in hours.
                    start = booking.time_slot.start_time
                    end = booking.time_slot.end_time

                    duration_minutes = (
                        end.hour * 60 + end.minute
                        - start.hour * 60 - start.minute
                    ) 

                    duration = Decimal(duration_minutes) / Decimal("60")

                    amount = court.price_per_hour * duration

                    # Create payment for the booking.
                    Payment.objects.create(
                        booking=booking,
                        amount=amount,
                        status=Payment.PaymentStatus.PENDING
                    )

                messages.success(
                    request,
                    "Booking created! Please complete your payment."
                )
                return redirect("pay_booking", booking_id=booking.id)

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
        .prefetch_related("payment")
        .order_by("-time_slot__date", "-time_slot__start_time")
    )

    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings
    })


@login_required
def cancel_booking(request, booking_id):
    if request.method != "POST":
        return redirect("my_bookings")

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.status not in [
        Booking.BookingStatus.PENDING,
        Booking.BookingStatus.CONFIRMED,
    ]:
        messages.error(request, "This booking cannot be cancelled.")
        return redirect("my_bookings")

    booking.status = Booking.BookingStatus.CANCELLED
    booking.save(update_fields=["status"])

    messages.success(request, "Your booking has been cancelled.")

    return redirect("my_bookings")



@login_required
def change_booking(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("court", "time_slot"),
        id=booking_id,
        user=request.user
    )

    if booking.status not in [
        Booking.BookingStatus.PENDING,
        Booking.BookingStatus.CONFIRMED,
    ]:
        messages.error(request, "This booking cannot be changed.")
        return redirect("my_bookings")

    if request.method == "POST":
        form = BookingForm(
            request.POST,
            court=booking.court,
            booking=booking
        )

        if form.is_valid():
            new_time_slot = form.cleaned_data["time_slot"]

            try:
                with transaction.atomic():
                    # Lock the booking while changing its time slot.
                    booking = Booking.objects.select_for_update().get(
                        id=booking.id,
                        user=request.user
                    )

                    booking.time_slot = new_time_slot
                    booking.save(update_fields=["time_slot"])

                messages.success(
                    request,
                    "Your booking time has been changed successfully!"
                )
                return redirect("my_bookings")

            except IntegrityError:
                messages.error(
                    request,
                    "Sorry, this time slot is no longer available."
                )
    else:
        form = BookingForm(
            court=booking.court,
            booking=booking,
            initial={"time_slot": booking.time_slot}
        )

    return render(request, "bookings/change_booking.html", {
        "form": form,
        "booking": booking,
    })


@login_required
def pay_booking(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("court", "time_slot"),
        id=booking_id,
        user=request.user
    )

    if booking.status != Booking.BookingStatus.PENDING:
        messages.error(request, "This booking cannot be paid for.")
        return redirect("my_bookings")

    payment = get_object_or_404(Payment, booking=booking)

    if payment.status == Payment.PaymentStatus.PAID:
        messages.info(request, "This booking has already been paid.")
        return redirect("my_bookings")

    if request.method == "POST":
        with transaction.atomic():
            payment.status = Payment.PaymentStatus.PAID
            payment.save(update_fields=["status"])

            booking.status = Booking.BookingStatus.CONFIRMED
            booking.save(update_fields=["status"])

        messages.success(request, "Payment successful! Your booking is confirmed.")
        return redirect("my_bookings")

    return render(request, "bookings/pay_booking.html", {
        "booking": booking,
        "payment": payment,
    })
