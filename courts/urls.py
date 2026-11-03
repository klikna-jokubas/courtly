from django.urls import path
from . import views

urlpatterns = [
    path("", views.court_list, name="court_list"),
    path("courts/<int:court_id>/", views.court_detail, name="court_detail"),
]