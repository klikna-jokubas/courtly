from django.shortcuts import render
from .models import Court
from django.shortcuts import render, get_object_or_404


def court_list(request):
    courts = Court.objects.filter(is_active=True)

    return render(request, "courts/court_list.html", {
        "courts": courts
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