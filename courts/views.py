
from django.shortcuts import render, get_object_or_404
from .models import Court, SportType


def court_list(request):
    courts = Court.objects.filter(is_active=True)

    selected_sport = request.GET.get("sport")
    selected_city = request.GET.get("city")

    if selected_sport:
        courts = courts.filter(sport_type_id=selected_sport)

    if selected_city:
        courts = courts.filter(
            sport_center__address__city__icontains=selected_city
        )

    sport_types = SportType.objects.all()

    cities = (
        Court.objects.filter(is_active=True)
        .values_list("sport_center__address__city", flat=True)
        .distinct()
    )

    return render(request, "courts/court_list.html", {
        "courts": courts,
        "sport_types": sport_types,
        "cities": cities,
        "selected_sport": selected_sport,
        "selected_city": selected_city,
    })


def court_detail(request, court_id):
    court = get_object_or_404(
        Court,
        id=court_id,
        is_active=True
    )

    return render(request, "courts/court_detail.html", {
        "court": court
    })
