
from django.test import TestCase
from django.urls import reverse

from .models import SportType, Address, SportCenter, Court


class CourtTests(TestCase):

    def setUp(self):
        self.tennis = SportType.objects.create(
            name="Tenisas",
            description="Teniso aikštelės"
        )

        self.football = SportType.objects.create(
            name="Futbolas",
            description="Futbolo aikštelės"
        )

        self.vilnius_address = Address.objects.create(
            city="Vilnius",
            street="Gedimino",
            building_number="1",
            postal_code="01103"
        )

        self.kaunas_address = Address.objects.create(
            city="Kaunas",
            street="Laisves",
            building_number="10",
            postal_code="44250"
        )

        self.vilnius_center = SportCenter.objects.create(
            name="Vilniaus sporto centras",
            description="Sporto centras Vilniuje",
            address=self.vilnius_address
        )

        self.kaunas_center = SportCenter.objects.create(
            name="Kauno sporto centras",
            description="Sporto centras Kaune",
            address=self.kaunas_address
        )

        self.tennis_court = Court.objects.create(
            sport_center=self.vilnius_center,
            sport_type=self.tennis,
            name="Teniso aikštelė",
            description="Teniso aikštelė Vilniuje",
            price_per_hour=20.00,
            is_active=True
        )

        self.football_court = Court.objects.create(
            sport_center=self.kaunas_center,
            sport_type=self.football,
            name="Futbolo aikštelė",
            description="Futbolo aikštelė Kaune",
            price_per_hour=30.00,
            is_active=True
        )

    # TA-02 / FR-02: Aikštelės informacijos peržiūra
    def test_court_detail(self):
        response = self.client.get(
            reverse("court_detail", args=[self.tennis_court.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teniso aikštelė")
        self.assertContains(response, "Vilniaus sporto centras")

    # TA-03 / FR-03: Filtravimas pagal sporto šaką
    def test_filter_by_sport(self):
        response = self.client.get(
            reverse("court_list"),
            {"sport": self.tennis.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teniso aikštelė")
        self.assertNotContains(response, "Futbolo aikštelė")

    # TA-04 / FR-04: Filtravimas pagal miestą
    def test_filter_by_city(self):
        response = self.client.get(
            reverse("court_list"),
            {"city": "Vilnius"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teniso aikštelė")
        self.assertNotContains(response, "Futbolo aikštelė")

    # TA-05 / FR-06: Filtrų pašalinimas
    def test_clear_filters(self):
        response = self.client.get(reverse("court_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teniso aikštelė")
        self.assertContains(response, "Futbolo aikštelė")
