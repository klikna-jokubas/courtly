
from django.urls import path

from . import views

urlpatterns = [
    path(
        "court/<int:court_id>/",
        views.create_booking,
        name="create_booking"
    ),
    path(
        "my/",
        views.my_bookings,
        name="my_bookings"
    ),
    path(
    "<int:booking_id>/cancel/",
    views.cancel_booking,
    name="cancel_booking"
    ),
    path(
    "<int:booking_id>/change/",
    views.change_booking,
    name="change_booking"
    ),
    path(
    "<int:booking_id>/pay/",
    views.pay_booking,
    name="pay_booking"
    ),
]
